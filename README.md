# Mesh Integrity Toolkit

A set of tools to fix common topology issues, such as vertices overlapping edges and overlapping faces.

## **Connect Overlaps Tool**

I created this tool after searching through countless add-ons for mesh cleaning and correction without finding anything that met my specific needs.
In short, the tool detects a vertex overlapping an edge and connects it.
Unlike Merge by Distance, which requires two nearby vertices to merge, this tool detects a vertex that lies along an edge it does not belong to. Once detected, the script subdivides that edge and snaps the new vertex to the position of the detected one, then runs bmesh.ops.remove_doubles to merge them into a single connected vertex.

**Demo**

https://github.com/user-attachments/assets/ab7ce742-f479-4e59-b93b-91d27438eef7

## Future Improvements

- **Performance (O(V×E) complexity):** The current detection loop iterates over all vertex-edge pairs, which can be slow on high-polygon meshes. A spatial acceleration structure (e.g. mathutils.kdtree) could significantly reduce lookup time.
- **Exposed threshold parameter:** threshold_distance is currently hardcoded at 0.001. Exposing it as a FloatProperty in the operator UI would allow per-case adjustment without touching the source.
- **Imprint Overlapping Faces tool:** A companion tool for edge-edge intersection detection is in early development and will be added in a future release.

