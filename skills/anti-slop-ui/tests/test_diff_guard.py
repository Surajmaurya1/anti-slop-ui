#!/usr/bin/env python3
"""Tests for scripts/diff_guard.py against a real React/TS fixture in a throwaway git repo.

Run:  python3 tests/test_diff_guard.py
Needs: git, Python 3.8+. No network, no third-party packages.

What this proves: the *tool* flags the behaviour changes listed below and stays
quiet on legitimate visual edits. What it does NOT prove: that any AI agent
follows the policy. See tests/scenarios.md for that status.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
GUARD = os.path.join(HERE, "..", "scripts", "diff_guard.py")
FIXTURE = os.path.join(HERE, "fixtures", "sample-app")
SIGNUP = "src/components/SignupForm.tsx"
DASH = "src/components/Dashboard.tsx"
CSS = "src/styles/app.css"


def git(repo, *args):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
                   cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def edit(repo, rel, old, new, count=1):
    p = os.path.join(repo, rel)
    with open(p, encoding="utf-8") as fh:
        s = fh.read()
    assert old in s, "fixture drifted: %r not in %s" % (old, rel)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(s.replace(old, new, count))


class Base(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp(prefix="asui-")
        shutil.copytree(FIXTURE, self.repo, dirs_exist_ok=True)
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "baseline")

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)

    def guard(self):
        p = subprocess.run([sys.executable, GUARD, "--repo", self.repo, "--json"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        data = json.loads(p.stdout)
        return p.returncode, data["findings"], data

    def cats(self, findings, sev=None):
        return {(f["category"]) for f in findings if sev is None or f["severity"] == sev}


class TestLegitimateVisualWork(Base):
    def test_restyle_classes_layout_css_is_clean(self):
        # change colours/spacing/radius, add wrapper markup, add aria-label, add visual import, edit CSS
        edit(self.repo, SIGNUP, 'className="flex flex-col gap-3 p-4 border rounded"',
             'className="mx-auto flex max-w-sm flex-col gap-5 rounded-xl border border-zinc-200 bg-white p-6 shadow-sm"')
        edit(self.repo, SIGNUP, 'className="bg-black text-white px-3 py-2 rounded"',
             'className="rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-indigo-500 focus-visible:ring-2"')
        edit(self.repo, SIGNUP, "<form onSubmit", "<div className=\"grid place-items-center\"><form aria-label=\"Create account\" onSubmit")
        edit(self.repo, SIGNUP, "</form>", "</form></div>")
        edit(self.repo, SIGNUP, 'import { useState } from "react";', 'import { useState } from "react";\nimport "../styles/app.css";')
        edit(self.repo, DASH, 'className="p-4"', 'className="mx-auto max-w-3xl p-6"')
        edit(self.repo, CSS, ".card { padding: 1rem;", ".card { padding: 1.5rem; border-radius: 12px;")
        rc, findings, _ = self.guard()
        self.assertEqual(rc, 0, findings)
        self.assertEqual(self.cats(findings, "HIGH") | self.cats(findings, "REVIEW"), set())

    def test_reformatting_same_tokens_is_clean(self):
        edit(self.repo, DASH, "{items.map((i) => (<li key={i.id}>{i.title}</li>))}",
             "{items.map((i) => (\n            <li key={i.id}>{i.title}</li>\n          ))}")
        rc, findings, _ = self.guard()
        self.assertEqual(rc, 0, findings)


class TestBehaviourChangesAreCaught(Base):
    def assertFlags(self, category, sev="HIGH"):
        rc, findings, _ = self.guard()
        self.assertIn(category, self.cats(findings, sev), "expected %s/%s, got %s" % (sev, category, findings))
        self.assertEqual(rc, 1 if sev == "HIGH" else 2)

    def test_removed_click_handler(self):
        edit(self.repo, DASH, "<button onClick={() => setOpen(!open)} className", "<button className")
        self.assertFlags("event-handler")

    def test_changed_handler_target(self):
        edit(self.repo, SIGNUP, "onSubmit={handleSubmit}", "onSubmit={() => {}}")
        self.assertFlags("event-handler")

    def test_changed_api_url(self):
        edit(self.repo, DASH, 'fetch("/api/items")', 'fetch("/api/v2/items")')
        self.assertFlags("data-access")

    def test_removed_effect_hook(self):
        edit(self.repo, DASH, "  useEffect(() => {\n    fetch(\"/api/items\").then((r) => r.json()).then(setItems);\n  }, []);\n", "")
        rc, findings, _ = self.guard()
        self.assertIn("hook", self.cats(findings, "HIGH"))
        self.assertIn("data-access", self.cats(findings, "HIGH"))

    def test_changed_route_target(self):
        edit(self.repo, SIGNUP, '<Link to="/login"', '<Link to="/sign-in"')
        self.assertFlags("routing/form-target")

    def test_removed_required_and_validation(self):
        edit(self.repo, SIGNUP, "type=\"email\" required value", "type=\"email\" value")
        self.assertFlags("form-attr")

    def test_removed_validation_logic(self):
        edit(self.repo, SIGNUP, '    if (!/^\\S+@\\S+$/.test(email)) {\n      setError("Enter a valid email");\n      return;\n    }\n', "")
        rc, findings, _ = self.guard()
        self.assertEqual(rc, 1)
        self.assertIn("state-update", self.cats(findings, "HIGH"))

    def test_changed_props_contract(self):
        edit(self.repo, SIGNUP, 'plan: "free" | "pro";', 'plan?: "free" | "pro";')
        self.assertFlags("component-contract")

    def test_replacing_form_with_static_markup(self):
        edit(self.repo, SIGNUP, "<form onSubmit={handleSubmit} className", "<div className")
        edit(self.repo, SIGNUP, "</form>", "</div>")
        rc, findings, _ = self.guard()
        self.assertEqual(rc, 1)
        cats = self.cats(findings, "HIGH")
        self.assertIn("form", cats)
        self.assertIn("event-handler", cats)

    def test_dependency_and_env_files(self):
        edit(self.repo, "package.json", '"react": "^18.3.1"', '"react": "^18.3.1", "left-pad": "^1.3.0"')
        edit(self.repo, ".env.example", "http://localhost:3000", "http://localhost:4000")
        rc, findings, _ = self.guard()
        self.assertEqual(rc, 2, findings)
        self.assertEqual({f["file"] for f in findings if f["category"] == "non-visual-file"}, {"package.json", ".env.example"})

    def test_new_non_visual_import_needs_review(self):
        edit(self.repo, DASH, 'import { useEffect, useState } from "react";',
             'import { useEffect, useState } from "react";\nimport { track } from "analytics-lib";')
        self.assertFlags("import-change", "REVIEW")

    def test_hiding_a_control_with_a_class_needs_review(self):
        edit(self.repo, DASH, 'className="border px-2 py-1">Toggle', 'className="hidden border px-2 py-1">Toggle')
        self.assertFlags("hides-ui", "REVIEW")

    def test_hiding_with_css_needs_review(self):
        edit(self.repo, CSS, ".card-title { font-weight: 500; }", ".card-title { font-weight: 500; display: none; }")
        self.assertFlags("hides-ui", "REVIEW")

    def test_untracked_new_file_with_fetch_is_scanned(self):
        with open(os.path.join(self.repo, "src/components/Widget.tsx"), "w") as fh:
            fh.write('export function W() {\n  fetch("/api/track");\n  return <div className="p-2" />;\n}\n')
        self.assertFlags("data-access")

    def test_deleted_source_file(self):
        os.remove(os.path.join(self.repo, DASH))
        rc, findings, _ = self.guard()
        self.assertEqual(rc, 1)
        self.assertIn("file-deleted", self.cats(findings, "HIGH"))


class TestKnownLimits(Base):
    def test_documented_limit_semantic_swap_of_literal_text_is_not_detected(self):
        # Changing visible copy is allowed (it is not behaviour). The tool must not flag it.
        edit(self.repo, SIGNUP, ">Sign up<", ">Create account<")
        rc, findings, _ = self.guard()
        self.assertEqual(rc, 0, findings)


if __name__ == "__main__":
    unittest.main(verbosity=2)
