import argparse

import numpy as np

import genesis as gs

def run_sim(scene,enable_vis):
    for i in range(1000):
        scene.step()
    if enable_vis:
        scene.viewer.stop()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vis", action="store_true", default=False)
    parser.add_argument("-c", "--cpu", action="store_true", default=False)
    args = parser.parse_args()

    ########################## init ##########################
    gs.init(backend=gs.cpu if args.cpu else gs.gpu, logging_level="debug")

    ########################## create a scene ##########################

    scene = gs.Scene(
        sim_options=gs.options.SimOptions(
            substeps=10,
            gravity=(0, 0, -9.8),
        ),
        viewer_options=gs.options.ViewerOptions(
            camera_pos=(2, 2, 1.5),
            camera_lookat=(0, 0, 0.5),
            camera_up=(0, 0, 1),
        ),
        show_viewer=args.vis,
    )

    ########################## materials ##########################
    mat_elastic = gs.materials.PBD.Elastic()

    ########################## entities ##########################

    bunny = scene.add_entity(
        material=mat_elastic,
        morph=gs.morphs.Mesh(
            file="meshes/dragon/dragon.obj",
            scale=0.1,
            pos=(0, 0, 0.8),
            euler = (0,0,1),
        ),
        surface=gs.surfaces.Default(
            # vis_mode='recon',
        ),
    )
    ########################## build ##########################
    scene.build()

    # horizon = 1000
    # # forward pass
    # for i in range(horizon):
    #     scene.step()
    gs.tools.run_in_another_thread(
        fn = run_sim,
        args = (scene,args.vis)
    )

    scene.viewer.start()

if __name__ == "__main__":
    main()
