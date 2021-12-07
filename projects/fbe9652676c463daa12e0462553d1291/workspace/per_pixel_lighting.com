{
#Example per_pixel_lighting.com:  Using per pixel lighting in CMISS.

# Using ARB Vertex programs and ARB Fragment programs per pixel lighting has
# been added into CMISS.  This example demostrates how to use these features.
# These examples have been tested on an NVIDIA FX card with Linux drivers 53.36
# and on Mesa3D 6.0 with a few patches (which have been submitted to the Mesa3D project).

$discretisation = "6*6*6";
$circle_discretisation = "12";

gfx modify scene default manual;

gfx read node $example/full_heart_press_0_def.exnode time 0;
gfx read element $example/full_heart_press_0_def.exelem;

gfx cre egroup septum add 9000014..9000021,9000032..9000034,9000037,9000043,9000051..9000052;
gfx cre egroup rv_free add 9000022,9000026,9000023..9000025,9000027,9000036,9000045..9000050,9000055;
gfx cre egroup lv_free add 9000004..9000013,9000028,9000029,9000030,9000031,9000035,9000039,9000040,9000041,9000042,9000053,9000054,9000057,9000059,9000061..9000062,9000065..9000069;

#gfx cre egroup base_skeletal add 9000082,9000083,9000084,9000085,9000086,9000087,9000088
gfx cre egroup base_skeletal_outer add 9000001,9000004,9000009,9000041,9000048..9000050,9000055..9000058,9000081;
gfx cre egroup base_skeletal_lower add 9000032..9000034,9000051..9000052;
gfx cre egroup base_muscle add 9000001,9000004,9000009,9000032..9000034,9000041,9000048..9000052,9000055..9000058,9000081;

gfx read node $example/MRP01.exnode;
gfx read element $example/MRP01.exelem;
gfx read element $example/MRP01_base.exelem;

gfx define field scaling_deformed scale field deformed scale 2.0 2.0 2.0;
gfx define field scaling_coordinates scale field coordinates scale 2.0 2.0 2.0;

gfx create texture heart_wall image $example/rc_text2.jpg mod;
gfx create material muscle diffuse 0.9 0.1 0.0 ambient 0.5 0 0 specular 0.6 0.6 0.6 shininess 0.95;
#gfx create material muscle texture heart diffuse 0.9 0.9 0.9 ;
gfx create material skeletal ambient 0 0 0 diffuse 1 0.3 0.23 emission 0 0 0 specular 0.3 0.3 0.3 alpha 1 shininess 0.3

# Map the 3D coordinates into cylindrical texture coordinates.  The texture coordinates have a seam where
# they wrap from 1 back to -1, I have aligned this with the seam at the edge of the texture.
gfx define field cylindrical_texture_coordinatesA coordinate_system rectangular_cartesian offset field coordinates offsets 0 0 -99.9464;
gfx define field cylindrical_texture_coordinatesB coordinate_system rectangular_cartesian composite cylindrical_texture_coordinatesA.2 cylindrical_texture_coordinatesA.1 cylindrical_texture_coordinatesA.3
gfx define field cylindrical_texture_coordinatesC coordinate_system rectangular_cartesian scale field cylindrical_texture_coordinatesB scale_factors 1.0 -1.0 1.0;
gfx define field cylindrical_texture_coordinatesD coordinate_system cylindrical_polar coordinate_transformation field cylindrical_texture_coordinatesC;
gfx define field cylindrical_texture_coordinatesE coordinate_system rectangular_cartesian composite cylindrical_texture_coordinatesD.2 cylindrical_texture_coordinatesD.3 cylindrical_texture_coordinatesD.1;
gfx define field cylindrical_texture_coordinatesF coordinate_system rectangular_cartesian scale field cylindrical_texture_coordinatesE scale_factors -0.159155 -0.0123 0.03;
gfx define field cylindrical_texture_coordinates coordinate_system rectangular_cartesian offset field cylindrical_texture_coordinatesF offsets -0.5 0 0;

gfx create scene heart manual;

gfx draw group lv_free scene heart;
gfx modify g_element lv_free general clear circle_discretization $circle_discretisation default_coordinate scaling_deformed element_discretization $discretisation native_discretization none scene heart;
gfx modify g_element lv_free surfaces face xi3_0 select_on material muscle selected_material default_selected render_shaded scene heart;

gfx draw group rv_free scene heart;
gfx modify g_element rv_free general clear circle_discretization $circle_discretisation default_coordinate scaling_deformed element_discretization $discretisation native_discretization none scene heart;
gfx modify g_element rv_free surfaces face xi3_0 select_on material muscle selected_material default_selected render_shaded scene heart;

gfx draw group septum scene heart;
gfx modify g_element septum general clear circle_discretization $circle_discretisation default_coordinate scaling_deformed element_discretization $discretisation native_discretization none scene heart;
gfx modify g_element septum surfaces face xi3_0 select_on material muscle selected_material default_selected render_shaded scene heart;
gfx modify g_element septum surfaces face xi3_1 select_on material muscle selected_material default_selected render_shaded scene heart;



gfx draw group wall scene heart;
gfx modify g_element wall general clear circle_discretization $circle_discretisation default_coordinate scaling_deformed element_discretization $discretisation native_discretization none scene heart;
#gfx modify g_element wall cylinders constant_radius 0.3 select_on material default selected_material default_selected scene heart;
gfx modify g_element wall surfaces select_on material muscle texture_coordinates cylindrical_texture_coordinates selected_material default_selected render_shaded scene heart exterior;


gfx draw group base_muscle scene heart;
gfx draw group base_skeletal scene heart;
gfx draw group base_skeletal_outer scene heart;
gfx draw group base_skeletal_lower scene heart;
gfx modify g_element base_muscle general clear circle_discretization $circle_discretisation default_coordinate scaling_coordinates element_discretization $discretisation native_discretization none scene heart



gfx modify g_element base_skeletal general clear circle_discretization $circle_discretisation default_coordinate scaling_coordinates element_discretization $discretisation native_discretization none scene heart
gfx modify g_element base_skeletal surfaces select_on material skeletal selected_material default_selected render_shaded scene heart


gfx modify g_element base_skeletal_outer general clear circle_discretization $circle_discretisation default_coordinate scaling_coordinates element_discretization $discretisation native_discretization none scene heart
gfx modify g_element base_skeletal_outer surfaces face xi2_1 select_on material skeletal selected_material default_selected render_shaded as musclele scene heart
gfx modify g_element base_skeletal_outer surfaces face xi2_1 select_on material muscle selected_material default_selected render_shaded as skeletaletal scene heart



gfx modify g_element base_skeletal_lower general clear circle_discretization $circle_discretisation default_coordinate scaling_coordinates element_discretization $discretisation native_discretization none scene heart
gfx modify g_element base_skeletal_lower surfaces face xi2_1 select_on material skeletal selected_material default_selected render_shaded as muscle scene heart
gfx modify g_element base_skeletal_lower surfaces face xi2_1 select_on material muscle selected_material default_selected render_shaded as skeletal scene heart

# Normal gouraud shading.  Next create a window and render this normally.
# We can see the Gouraud shading artefacts most clearly on the specular highlights
# which have been stretched into star like patterns.

gfx create window 1;
gfx modify window 1 image scene heart;
gfx modify window 1 view parallel eye_point -446.961 -114.755 -5.34199 interest_point 4.41712 7.8208 115.947 up_vector 0.217583 0.152671 -0.964028 view_angle 28.5452 near_clipping_plane 4.83196 far_clipping_plane 1726.78 relative_viewport ndc_placement -1 1 2 2 viewport_coordinates 0 0 1 1;

# Per Pixel Lighting.
# If supported by your OpenGL implementation the muscle material will change to per pixel lighting.
# Currently the implementation is equivalent to the old model of point lighting, so we shift the
# point light to a position which gives lighting similar to the default directional light.
# Notice the defined specular highlights and how they move as you rotate the model.
gfx modify material muscle per_pixel_mode;
gfx modify light default point position 0 100 -100;
if ($TESTING)
  {
	 gfx print win 1 file per_pixel.jpg anti 8;
  }

# Texturing
# We can add textures into this model.  Currently this only supports the equivalent of the old modulate
# texture mode, so we change the background material to white so that the modulated texture is equivalent
# to the texture.  Notice how the specular highlights are visible on this textured model unlike with
# standard OpenGL as in our Fragment Program implementation these are added on to the textured colour,
# whereas the specular highlights on the standard OpenGL implementation are just added to the colour
# prior to texturing and lost.

gfx modify material muscle per_pixel_mode texture heart_wall diffuse 1 1 1 ambient 0.1 0.1 0.1;
if ($TESTING)
  {
	 gfx print win 1 file per_pixel_texture.jpg anti 8;
  }

# We can also specify any arbitrary program strings,
# this requires to you write all the graphics operations yourself but gives
# you complete flexibility.  Be aware that changes to cmgui could break your
# programs in their assumptions about input variables and so you may have to migrate
# your changes occasionally.
CORE::open VPFILE, "<$example/vp.txt";
@vp = <VPFILE>;
CORE::open FPFILE, "<$example/fp.txt";
@fp = <FPFILE>;
#The last line of fp.txt is modified to reorder the colours so that this material
#is greeny coloured and therefore different from the standard per pixel texturing.
gfx modify material muscle vertex_program_string join("",@vp) fragment_program_string join("",@fp);

if ($TESTING)
{
    #Check commands allow updating of some parts correctly
	gfx mod material muscle;
	gfx mod material muscle vertex_program_string join("",@vp);
	gfx print win 1 file per_pixel_user_program.jpg anti 8;
}

# Change back to normal lighting to see the difference
gfx modify material muscle normal_mode;

# Bump mapping
# Now that we have per pixel control over the lighting in the fragment program we can modulate
# the surface normal with a normal map.  This normal map I produced in Gimp from the colour texture
# using the Filter->Map->Normal_map plugin from http://nifelheim.dyndns.org/~cocidius/normalmap/
# A normal map uses the colour channels to specify variations in normal direction from the surface
# coordinates.

gfx create texture heart_wall_normal_map image $example/rc_text2_normalmap.jpg;
gfx modify material muscle per_pixel_mode texture heart_wall secondary_texture heart_wall_normal_map bump_mapping;
if ($TESTING)
  {
	 gfx print win 1 file per_pixel_texture_bump.jpg anti 8;
  }

# The rapidly varying texture map adds an organic and wet quality to the model.
# As the normal map is actually based on the colour image rather than a real height field it is 
# actually incorrect but if we had a height map for our model that could be used to make the
# normal map instead.


}