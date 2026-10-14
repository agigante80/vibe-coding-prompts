# Label Taxonomy

GitHub labels serve dual purpose: issue organization AND lens routing in ticket-gate (which lenses join the critic, and how its brief is modulated).

## Label categories

### Type labels
| Label | Description | Creates in GitHub |
|---|---|---|
| `bug` | Something isn't working | Yes |
| `enhancement` / `feature` | New feature or request | Yes |
| `security` | Security vulnerability or hardening | Yes - adds the security lens |
| `infrastructure` | DevOps, CI/CD, deployment | Yes |
| `design` | Wireframes, UX, accessibility | Yes |
| `documentation` | Docs updates | Yes |
| `testing` | Tests, QA, coverage | Yes |

### Area labels (modulate the gate's review set)
| Label | Description | Triggers |
|---|---|---|
| `prompts` | Prompt files in prompts/, new or changed meta-prompts | - |
| `docs` | Concept guides in docs/ and the root README | - |
| `tooling` | The guards, scripts and CI that enforce the rules | - |
| `governance` | Templates, labels, ticket standards, the roadmap and the docs that carry them | - |

Label names match without regard to case in the gate's lens routing and its labels check, so a project
that spells an area `API` or `Privacy` still gets the `api` and `privacy` behaviour (#472). Only names
this table lists are folded, so `Apiary` is not `api`.
The type label that picks the template in `forge-gate-mechanics.sh` matches the same way, so a `Bug`
ticket is checked against `bug.yml` while `Bugfix` falls back to `feature.yml` (#476).

<!-- adapt-dropped: forge-kit-only -->

<!-- adapt-dropped: forge-kit-only -->

<!-- adapt-dropped: forge-kit-only -->

### Priority labels
| Label | Meaning |
|---|---|
| `P0` | Critical - blocks release |
| `P1` | High - important for current milestone |
| `P2` | Medium - should do, not blocking |
| `P3` | Low - nice to have |

### Special labels
| Label | Effect |
|---|---|
| `critical` | Adds the security lens and puts the critic in maximum scrutiny |

## Installing labels

After installing forge-kit, sync the taxonomy from `.github/labels.yml` with the shipped script:

```bash
# Run it from wherever it was installed; it sources forge-lib.sh from its OWN directory,
# so keep the two together (forge-adapt's Templates mode and the forge-host install each copy both).
bash sync-labels.sh                 # create every declared label, update any that drifted
bash sync-labels.sh --check         # change nothing; exit 1 listing what is missing or drifted
FORGE_DRY_RUN=1 bash sync-labels.sh # print what it would WRITE; it still READS the host, so
                                    # it needs credentials and reports against real state
```

It is host-aware (GitHub and Forgejo), idempotent, refuses a malformed declaration rather than
syncing part of it, and **never deletes**: a label on the host that
this file does not declare is reported and left alone.

<!-- adapt-dropped: forge-kit-only -->

## Adding project-specific labels

The area table above IS the set the gate checks against: both `ticket-gate` (Step 3A) and
`forge-gate-mechanics.sh` pass this file to `check-ticket-mechanics.sh --labels-doc`, and with
this file absent `ticket-gate` Step 0b runs the checker too, blocking a ticket whose `labels`
row fails (#425). The first column of the `### Area labels` table replaces the compiled-in default (#204). To add an area,
add a row to that table and the matching entry to your label declaration (`.github/labels.yml`
on GitHub; `sync-labels.sh` puts it on the host).

<!-- adapt-dropped: forge-kit-only -->

Without this file the checker falls back to forge-kit's nine and says so in the `labels` row
(`labels.md not found; using forge-kit's built-in nine areas...`). A label in neither the nine nor
the type set is then reported `referred`, for the gate's critic to judge, rather than failed; a
ticket carrying only type labels, or none, still fails, and Step 0b blocks it (#425). So a project
that renames its areas needs the doc installed, not only the labels:
```yaml
- name: my-domain
  color: "c5def5"
  description: My project-specific area
```

Then add the label as a trigger in `ticket-gate.md`'s lens table if it should route to a lens or modulate the critic's brief.
