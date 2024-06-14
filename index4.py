import gmsh
import sys

def initialize_gmsh():
    gmsh.initialize(sys.argv)
    gmsh.option.setNumber("General.Terminal", 1)
    gmsh.model.add("3d_extruded_model")

def prepare_mesh(file_path, extrusion_length, translation_z):
    try:
        gmsh.clear()
        gmsh.model.add("3d_extruded_model")
        gmsh.merge(file_path)
        gmsh.model.occ.synchronize()

        surfaces = gmsh.model.getEntities(2)
        if not surfaces:
            print(f"No surfaces found in {file_path}.")
            return None

        surface_tag = max(tag for dim, tag in surfaces if dim == 2)
        extruded_entities = gmsh.model.occ.extrude([(2, surface_tag)], 0, 0, extrusion_length)
        volume_tags = [tag for dim, tag in extruded_entities if dim == 3]
        if volume_tags:
            gmsh.model.occ.translate([(3, volume_tags[0])], 0, 0, translation_z)

        gmsh.model.occ.synchronize()
        gmsh.model.mesh.generate(3) # 2, 3  STL files are inherently surface mesh formats. Only surface elements are exported!

        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def save_mesh_as_file(file_path, format_type, stl_format):
    if format_type == 'obj':
        output_filename = file_path.replace('.step', '.obj')
    elif format_type == 'stl':
        output_filename = file_path.replace('.step', '.stl')
        gmsh.option.setNumber("Mesh.Binary", 1 if stl_format == 'binary' else 0)
    else:
        print(f"Unsupported file format: {format_type}")
        return None

    # Additional options
    gmsh.option.setNumber("Mesh.SaveAll", 1)  # Save all elements
    gmsh.option.setNumber("Mesh.SaveElementTagType", 3)  # Save as solid elements

    try:
        gmsh.write(output_filename)
        return output_filename
    except Exception as e:
        print(f"Failed to save {format_type} file: {e}")
        return None

def cleanup():
    gmsh.finalize()

def main():
    initialize_gmsh()

    max_mesh_size = 1.0
    gmsh.option.setNumber("Mesh.MeshSizeMax", max_mesh_size)

    output_format = 'stl'
    stl_format = 'binary'


    models = [
        ('./Rotor_Segment.step', 10.0, 0),
        ('./Stator_Segment.step', 5.0, 2.5)
    ]

    for file_path, extrusion_length, translation_z in models:
        print(f"Processing {file_path}...")
        if prepare_mesh(file_path, extrusion_length, translation_z):
            output_file = save_mesh_as_file(file_path, output_format, stl_format)
            print(f"Successfully processed and saved {output_file}")

    cleanup()

if __name__ == "__main__":
    main()
