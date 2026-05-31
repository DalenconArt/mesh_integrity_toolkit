# connect_overlaps.py

import bpy
import bmesh
from mathutils import Vector

class MESH_OT_connect_overlaps_auto(bpy.types.Operator):
    """Robustly and iteratively fixes mesh overlaps."""
    bl_idname = "mesh.connect_overlaps_auto"
    bl_label = "Connect Overlaps (Auto)" # Neutral and professional
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'EDIT'

    def execute(self, context):
        threshold_distance = 0.001
        obj = context.edit_object
        
        print("\n--- Starting mesh overlap analysis and correction ---")
        pass_counter = 0
        total_corrections = 0
        while True:
            pass_counter += 1
            if pass_counter > 100:
                print("Connect Operation: Safety limit of 100 passes reached. Stopping to prevent infinite loops.")
                break

            correction_made_in_this_pass = False
            
            bm = bmesh.from_edit_mesh(obj.data)
            bm.verts.ensure_lookup_table()
            
            task = None
            # Looking for a single overlap to process atomically
            for guide_vert in bm.verts:
                for target_edge in bm.edges:
                    if not target_edge.is_valid or guide_vert in target_edge.verts: continue
                    
                    v1, v2, p = target_edge.verts[0].co, target_edge.verts[1].co, guide_vert.co
                    line_vec, point_vec = v2 - v1, p - v1
                    if line_vec.length_squared == 0: continue
                    t = max(0, min(1, point_vec.dot(line_vec) / line_vec.length_squared))
                    dist = (p - (v1 + t * line_vec)).length
                    
                    if dist < threshold_distance:
                        task = {'guide_idx': guide_vert.index, 'target_edge_idx': target_edge.index}
                        break
                if task: break
            
            if task:
                print(f"  Pass {pass_counter}: Overlap identified (Vertex {task['guide_idx']} near Edge {task['target_edge_idx']}). Preparing correction...")
                try:
                    # Reloading the bmesh to ensure data consistency after modifications
                    bm.free()
                    bm = bmesh.from_edit_mesh(obj.data)
                    bm.verts.ensure_lookup_table()
                    bm.edges.ensure_lookup_table()

                    guide_vert = bm.verts[task['guide_idx']]
                    target_edge = bm.edges[task['target_edge_idx']]
                    guide_pos = guide_vert.co.copy()
                    
                    # 1. Subdividing the target edge to create a new vertex
                    ret = bmesh.ops.subdivide_edges(bm, edges=[target_edge], cuts=1)
                    new_vert = [v for v in ret['geom_inner'] if isinstance(v, bmesh.types.BMVert)][0]
                    
                    # 2. Aligning the new vertex with the guide vertex position
                    new_vert.co = guide_pos
                    print(f"    New intermediate vertex created and aligned for connection.")
                    
                    correction_made_in_this_pass = True
                    total_corrections += 1
                    
                    bmesh.update_edit_mesh(obj.data)
                except (IndexError, ReferenceError) as e:
                    print(f"    WARNING: Unexpected error during correction on pass {pass_counter}. Geometry may have changed. Error: {e}")
            
            # Mesh cleanup and consolidation after each correction attempt
            bm.free()
            bm = bmesh.from_edit_mesh(obj.data)
            
            # Print the consolidation message ONLY IF A CORRECTION WAS MADE,
            # or if we are on the first pass and want to ensure an initial cleanup.
            # The `pass_counter == 1` condition covers the case where no correction
            # is made but we still want an initial cleanup pass.
            if correction_made_in_this_pass or pass_counter == 1: # Added 'or pass_counter == 1' to ensure the message on the 1st pass
                print("    Consolidating geometry: Removing duplicate vertices and updating mesh.")
            
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
            bmesh.update_edit_mesh(obj.data)
            bm.free()

            if not correction_made_in_this_pass:
                print("  No new overlaps found in this pass. Correction process complete.")
                break # Exit the while loop

        # Final consolidation message, in case the loop ends without corrections on the last pass
        # and the message has not yet been displayed. The logic above already covers most cases.
        # A final 'remove_doubles' outside the loop, without a message, could ensure absolute cleanup.
        # In this case, the `remove_doubles` inside the loop is already sufficient.

        if total_corrections > 0:
            self.report({'INFO'}, f"Process complete: {total_corrections} mesh overlaps resolved.")
        else:
            self.report({'INFO'}, "No mesh overlaps detected. Your mesh is clean.")
            
        return {'FINISHED'}