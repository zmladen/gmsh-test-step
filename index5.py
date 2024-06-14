import re
import numpy as np
from pygltflib import GLTF2, Scene, Node, Mesh, Primitive, Accessor, Buffer, BufferView, Asset, Material, Attribute

def read_ascii_stl(filename):
    with open(filename, 'r') as f:
        content = f.read()

    vertex_pattern = re.compile(r'vertex\s+([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)\s+([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)\s+([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)')
    vertices = []
    for vertex in vertex_pattern.findall(content):
        vertices.append([float(vertex[0]), float(vertex[1]), float(vertex[2])])

    vertices = np.array(vertices, dtype=np.float32)
    indices = np.arange(len(vertices), dtype=np.uint32)
    
    return vertices, indices

def create_gltf(vertices, indices, color):
    num_vertices = len(vertices)
    num_indices = len(indices)
    
    # Create buffer
    vertex_buffer = vertices.tobytes()
    index_buffer = indices.tobytes()
    
    buffer = Buffer(byteLength=len(vertex_buffer) + len(index_buffer))
    buffer.uri = "data:application/octet-stream;base64," + (vertex_buffer + index_buffer).hex()

    # Create buffer views
    buffer_view_vertex = BufferView(buffer=0, byteOffset=0, byteLength=len(vertex_buffer), target=34962)
    buffer_view_index = BufferView(buffer=0, byteOffset=len(vertex_buffer), byteLength=len(index_buffer), target=34963)

    # Create accessors
    min_vertex = vertices.min(axis=0).tolist()
    max_vertex = vertices.max(axis=0).tolist()

    accessor_vertex = Accessor(bufferView=0, byteOffset=0, componentType=5126, count=num_vertices, type="VEC3", min=min_vertex, max=max_vertex)
    accessor_index = Accessor(bufferView=1, byteOffset=0, componentType=5125, count=num_indices, type="SCALAR", min=[0], max=[num_vertices - 1])

    # Create mesh
    primitive = Primitive(attributes=Attribute(POSITION=0), indices=1, material=0)
    mesh = Mesh(primitives=[primitive])

    # Create node
    node = Node(mesh=0)

    # Create scene
    scene = Scene(nodes=[0])

    # Create material
    # material = Material(pbrMetallicRoughness=PBRMetallicRoughness(baseColorFactor=color, metallicFactor=1, roughnessFactor=1))

    # Create glTF object
    gltf = GLTF2(asset=Asset(version="2.0"), buffers=[buffer], bufferViews=[buffer_view_vertex, buffer_view_index], accessors=[accessor_vertex, accessor_index], meshes=[mesh], nodes=[node], scenes=[scene])
    gltf.scenes.append(scene)
    gltf.nodes.append(node)

    return gltf

def convert_stl_to_glb(stl_filename, glb_filename, color=[1.0, 1.0, 1.0, 1.0]):
    vertices, indices = read_ascii_stl(stl_filename)
    gltf = create_gltf(vertices, indices, color)
    gltf.save(glb_filename)

# Example usage
stl_filename = "Rotor_Segment.stl"
glb_filename = "example.glb"
color = [0.588, 0.588, 0.588, 1.0]  # Example RGBA color

convert_stl_to_glb(stl_filename, glb_filename, color)
