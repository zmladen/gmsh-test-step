import gmsh
import sys

def initialize_gmsh():
    gmsh.initialize(sys.argv)
    gmsh.option.setNumber("General.Terminal", 1)
    gmsh.model.add("3d_extruded_model")

def merge_and_extrude(file_path, extrusion_length, translation_z):
    try:
        gmsh.merge(file_path)
        gmsh.model.occ.synchronize()
        surfaces = gmsh.model.getEntities(2)
        if not surfaces:
            print(f"No surfaces found in {file_path}.")
            return False

        surface_tag = max(tag for dim, tag in surfaces if dim == 2)
        extruded_entities = gmsh.model.occ.extrude([(2, surface_tag)], 0, 0, extrusion_length)
        volume_tags = [tag for dim, tag in extruded_entities if dim == 3]
        if volume_tags:
            gmsh.model.occ.translate([(3, volume_tags[0])], 0, 0, translation_z)
        gmsh.model.occ.synchronize()  # Synchronize after extrusion
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def generate_mesh(max_mesh_size):
    gmsh.option.setNumber("Mesh.MeshSizeMax", max_mesh_size)
    gmsh.model.mesh.generate(1)

    gmsh.write("3d_extruded_mesh.msh")

def export_mesh(format='stl'):
    if format == 'stl':
        gmsh.write("output_model.stl")
    else:
        gmsh.write("output_model.msh")

def cleanup():
    gmsh.fltk.run()
    gmsh.finalize()

def main():
    initialize_gmsh()

    # Mesh size configuration
    max_mesh_size = 3.0  # Maximum mesh size in millimeters

    # File paths and extrusion details
    models = [
        ('./Rotor_Segment.step', 10.0, 0),
        ('./Stator_Segment.step', 5.0, 2.5)
    ]

    for file_path, extrusion_length, translation_z in models:
        print(f"Processing {file_path}...")
        if not merge_and_extrude(file_path, extrusion_length, translation_z):
            gmsh.finalize()
            return
        print(f"Successfully processed {file_path}.")

    generate_mesh(max_mesh_size)
    export_mesh(format='stl')  # Change to ascii_stl=False for binary STL

    cleanup()

if __name__ == "__main__":
    main()
