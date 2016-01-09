
# Disable the "xxx has no yyy member" error, pylint seems to be unable to detect
# the properties of a nodepath
# pylint: disable=E1101

from __future__ import print_function

import os
import sys
import math
from random import random, randint, seed
from panda3d.core import Vec3, load_prc_file_data
from direct.showbase.ShowBase import ShowBase

# Change to the current directory
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__))))

# Append the current directory to the path
sys.path.insert(0, os.getcwd())


class MainApp(ShowBase):

    """ Main Testing Showbase """

    def __init__(self):

        # Setup window size, title and so on
        load_prc_file_data("", """
        win-size 1600 900
        window-title Render Pipeline by tobspr 
        icon-filename Data/GUI/icon.ico
        """)

        # ------ Begin of render pipeline code ------

        # Insert the pipeline path to the system path, this is required to be
        # able to import the pipeline classes
        pipeline_path = "../../"

        # Just a special case for my development setup, so I don't accidentally
        # commit a wrong path. You can remove this in your own programs.
        if not os.path.isfile(os.path.join(pipeline_path, "setup.py")):
            pipeline_path = "../../RenderPipeline/"
            
        sys.path.insert(0, pipeline_path)

        from __init__ import RenderPipeline, SpotLight
        from Code.Util.MovementController import MovementController

        self.render_pipeline = RenderPipeline(self)
        self.render_pipeline.create()

        # [Optional] use the default skybox, you can use your own skybox as well
        self.render_pipeline.create_default_skybox()

        # ------ End of render pipeline code, thats it! ------

        # Set time of day
        self.render_pipeline.get_daytime_mgr().set_time(0.52)

        # Load the scene
        model = loader.loadModel("scene/Scene.bam")
        model.reparent_to(render)

        # Temperature lamps
        for lumlamp in model.find_all_matches("**/LampLum*"):
            lum = float(lumlamp.get_name()[len("LampLum"):])
            light = SpotLight()
            light.direction = (0, 0, -1)
            light.fov = 70
            light.set_color_from_temperature(lum * 1000.0)
            light.lumens = 500.0
            light.pos = lumlamp.get_pos(self.render)
            light.radius = 10
            light.casts_shadows = True
            light.shadow_map_resolution = 512
            self.render_pipeline.add_light(light)

            panda = loader.loadModel("panda")
            panda.reparent_to(render)
            panda.set_pos(light.pos)
            panda.set_z(0.65)
            panda.set_h(180 + randint(-60, 60))
            panda.set_scale(0.2)
            panda.set_y(panda.get_y() + 1.0)


        # Load some fancy ies profile
        # ies_profile = self.render_pipeline.load_ies_profile("Data/IESProfiles/Defined.ies")
        
        # Add some random lights
        # sqr = 2
        # seed(3)
        # for x in range(sqr):
        #     for y in range(sqr):
        #         light = SpotLight()
        #         light.direction = (0, 0, -1)
        #         light.fov = 110.0
        #         light.set_color_from_temperature(6504)
        #         print(light.color)
        #         light.lumens = 1.0
        #         pos_x, pos_y = (x-sqr//2) * 7.0 + 5.0, (y-sqr//2) * 7.0 + 5.0
        #         light.pos = (pos_x, pos_y, 12.0)
        #         light.radius = 35.0
        #         light.casts_shadows = True
        #         light.near_plane = 0.1
        #         light.shadow_map_resolution = 512
        #         # light.ies_profile = ies_profile
        #         self.render_pipeline.add_light(light)

        # Init movement controller
        self.controller = MovementController(self)
        self.controller.set_initial_position(Vec3(3, 25, 8), Vec3(5, 0, 0))
        self.controller.setup()
        
MainApp().run()