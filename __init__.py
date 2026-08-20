# SPDX-License-Identifier: GPL-3.0-or-later

import bpy
import bmesh

from bpy.props import BoolProperty


def _quad_neighbors(faces):
    """Return selected-quad adjacency without relying on face indices."""
    face_set = set(faces)
    neighbors = {face: [] for face in faces}

    for face in faces:
        for edge in face.edges:
            for linked_face in edge.link_faces:
                if linked_face is not face and linked_face in face_set:
                    neighbors[face].append(linked_face)

    return neighbors


def _alternating_groups(faces):
    """Bipartition every connected selection island using breadth-first order."""
    neighbors = _quad_neighbors(faces)
    side = {}

    # Stable seeds make repeated execution predictable.
    for seed in sorted(faces, key=lambda face: face.index):
        if seed in side:
            continue

        side[seed] = 0
        queue = [seed]
        cursor = 0

        while cursor < len(queue):
            face = queue[cursor]
            cursor += 1
            next_side = 1 - side[face]

            for neighbor in sorted(neighbors[face], key=lambda item: item.index):
                if neighbor not in side:
                    side[neighbor] = next_side
                    queue.append(neighbor)

    return side


class MESH_OT_zigzag_triangulate(bpy.types.Operator):
    """Split selected quad regions with alternating diagonal directions"""

    bl_idname = "mesh.zigzag_triangulate"
    bl_label = "Zigzag Triangulate"
    bl_description = "Triangulate selected adjacent quads with alternating diagonals"
    bl_options = {"REGISTER", "UNDO"}

    reverse: BoolProperty(
        name="Reverse Pattern",
        description="Swap the two diagonal directions",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        obj = context.edit_object
        return obj is not None and obj.type == "MESH" and context.mode == "EDIT_MESH"

    def execute(self, context):
        obj = context.edit_object
        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces.ensure_lookup_table()
        bm.faces.index_update()

        selected = [face for face in bm.faces if face.select]
        quads = [face for face in selected if len(face.verts) == 4]
        skipped = len(selected) - len(quads)

        if not quads:
            self.report({"WARNING"}, "Select one or more quad faces")
            return {"CANCELLED"}

        groups = _alternating_groups(quads)

        # Triangulate one face at a time because each face needs its own method.
        # The topology grouping above is captured before any faces are replaced.
        for face in sorted(quads, key=lambda item: item.index):
            use_alternate = bool(groups[face]) ^ self.reverse
            result = bmesh.ops.triangulate(
                bm,
                faces=[face],
                quad_method="ALTERNATE" if use_alternate else "FIXED",
                ngon_method="BEAUTY",
            )
            for triangle in result.get("faces", []):
                triangle.select_set(True)

        bmesh.update_edit_mesh(obj.data, loop_triangles=True, destructive=True)

        message = f"Triangulated {len(quads)} quad face(s) in a zigzag pattern"
        if skipped:
            message += f"; skipped {skipped} non-quad face(s)"
        self.report({"INFO"}, message)
        return {"FINISHED"}


def _draw_face_context_menu(self, context):
    self.layout.separator()
    self.layout.operator(
        MESH_OT_zigzag_triangulate.bl_idname,
        text="Zigzag Triangulate",
        icon="MOD_TRIANGULATE",
    )


classes = (MESH_OT_zigzag_triangulate,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_edit_mesh_faces.append(_draw_face_context_menu)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(_draw_face_context_menu)


def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(_draw_face_context_menu)
    bpy.types.VIEW3D_MT_edit_mesh_faces.remove(_draw_face_context_menu)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

