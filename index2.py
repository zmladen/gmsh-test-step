import gmsh
import sys

def main():
    # Initialize Gmsh API
    gmsh.initialize(sys.argv)
    gmsh.option.setNumber("General.Terminal", 1)

    # Create a new model
    gmsh.model.add("3d_extruded_model")

    # Paths to the geometry files
    file1 = './Rotor_Segment.step'
    file2 = './Stator_Segment.step'

    # Extrusion lengths in millimeters
    extrusion_length_1 = 20.0  # 10 mm for the first extrusion
    extrusion_length_2 = 5.0   # 5 mm for the second extrusion

    # Z-axis translation distances
    translation_z_1 = 0  # Translate first extrusion by 20 mm in the Z direction
    translation_z_2 = 2.5  # Translate second extrusion by 40 mm in the Z direction


    # Try to merge the first file and extrude
    try:
        gmsh.merge(file1)
        gmsh.model.occ.synchronize()
        surfaces = gmsh.model.getEntities(2)
        if surfaces:
            first_surface_tag = max(tag for dim, tag in surfaces if dim == 2)
            # gmsh.model.occ.extrude([(2, first_surface_tag)], 0, 0, extrusion_length_1)
            extruded_entities = gmsh.model.occ.extrude([(2, first_surface_tag)], 0, 0, extrusion_length_1)

            # Find and translate the volume
            volume_tags = [tag for dim, tag in extruded_entities if dim == 3]
            if volume_tags:
                gmsh.model.occ.translate([(3, volume_tags[0])], 0, 0, translation_z_1)


        else:
            print("No surfaces found in the first file.")
    except Exception as e:
        print(f"Error processing first file: {e}")
        gmsh.finalize()
        return

    # Try to merge the second file and extrude
    try:
        gmsh.merge(file2)
        gmsh.model.occ.synchronize()
        surfaces = gmsh.model.getEntities(2)
        if surfaces:
            second_surface_tag = max(tag for dim, tag in surfaces if dim == 2)

            extruded_entities = gmsh.model.occ.extrude([(2, second_surface_tag)], 0, 0, extrusion_length_2)
            # Find and translate the volume
            volume_tags = [tag for dim, tag in extruded_entities if dim == 3]
            if volume_tags:
                gmsh.model.occ.translate([(3, volume_tags[0])], 0, 0, translation_z_2)

        else:
            print("No surfaces found in the second file.")
    except Exception as e:
        print(f"Error processing second file: {e}")
        gmsh.finalize()
        return

    # Synchronize to update the model with new entities
    gmsh.model.occ.synchronize()

    # Generate 3D mesh
    gmsh.model.mesh.generate(3)

    # Launch the GUI to view the mesh
    gmsh.fltk.run()

    # Save the mesh to file
    gmsh.write("3d_extruded_mesh.msh")

    # Clean up
    gmsh.finalize()

if __name__ == "__main__":
    main()