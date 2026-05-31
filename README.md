A set of tools to fix common topology issues, such as vertices overlapping edges and overlapping faces.

Connect Overlaps Tool
I created this tool after searching through countless add-ons for mesh cleaning and correction without finding anything that met my specific needs.
In short, the tool detects a vertex overlapping an edge and connects it.
Unlike Merge by Distance, which requires two nearby vertices to merge, this tool detects a vertex that lies along an edge it does not belong to. Once detected, the script subdivides that edge and snaps the new vertex to the position of the detected one, then runs bmesh.ops.remove_doubles to merge them into a single connected vertex.

https://github.com/user-attachments/assets/ab7ce742-f479-4e59-b93b-91d27438eef7

