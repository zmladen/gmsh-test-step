import gmsh
import sys

def main():
    # Initialize Gmsh API
    gmsh.initialize(sys.argv)
    gmsh.option.setNumber("General.Terminal", 1)

    # Create a new model
    gmsh.model.add("2d_step_model")

    # Merge the STEP file
    path_to_step_file = './Stator_Segment.step'
    
    try:
        gmsh.merge(path_to_step_file)
    except Exception as e:
        print(f"An error occurred while merging the STEP file: {e}")
        gmsh.finalize()
        return

    # Synchronize necessary before meshing
    gmsh.model.geo.synchronize()

    # Set mesh algorithm (optional, for example to use Delaunay)
    gmsh.option.setNumber("Mesh.Algorithm", 5)  # Delaunay for 2D

    # Generate 2D mesh
    gmsh.model.mesh.generate(2)

    # Launch the GUI to view the mesh
    gmsh.fltk.run()

    # Save the mesh to file (optional)
    gmsh.write("2d_mesh.msh")

    # Clean up
    gmsh.finalize()

if __name__ == "__main__":
    main()
