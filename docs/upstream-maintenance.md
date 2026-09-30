# Public skills and upstream updates

The first version contains authored skills only. upstreams.json records public imports when selected; upstream/ is reserved for imported content. No upstream synchronisation automation is implemented yet.

For each import, record a unique id, repository URL, source path, destination path under upstream/, exact base commit, license identifier/file, and whether the copy has local adaptations. Retain required attribution and license files. Do not import a public skill without checking its licensing.

Import the selected skill at the recorded commit, review the complete method, run structural checks, and exercise it before relying on it. Install selected imported skill directories explicitly; scripts/link.py currently links authored skills only.

For an update, compare three versions: the recorded upstream base, the new upstream revision, and the locally maintained copy. Review behaviour and reconcile local changes rather than replacing the directory blindly. Update the recorded base only with the reconciled import. Keep the import/update and its provenance change in the same commit. A fully owned fork can stop taking updates, but should retain origin and license information.

The precise fetching mechanism is deliberately deferred until the first selected upstream gives us a real maintenance case.
