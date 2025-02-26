import argparse

import numpy as np

import genesis as gs

def run_sim(scene, cam, enable_vis):
    horizon = 1000
    
    cam.start_recording()

    for i in range(horizon):
        scene.step()
        cam.render()

    if enable_vis:
        scene.viewer.stop()
    cam.stop_recording(save_to_filename ="cloth_reverse.mp4")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vis", action="store_true", default=False)
    parser.add_argument("-c", "--cpu", action="store_true", default=False)
    args = parser.parse_args()

    ########################## init ##########################
    gs.init(seed=0, precision="32", logging_level="debug", backend=gs.cpu if args.cpu else gs.gpu)

    scene = gs.Scene(
        sim_options=gs.options.SimOptions(
            dt=2e-3,
            substeps=50,
            gravity = (0 , 0, -9.81),
        ),
        pbd_options=gs.options.PBDOptions(
            particle_size=1e-2,
            lower_bound=(-1.0, -1.0, -0.3),
            upper_bound=(1.0, 1.0, 1.0),
        ),
        mpm_options= gs.options.MPMOptions(
            lower_bound=(-1.0, -1.0, -0.3),
            upper_bound=(1.0, 1.0, 1.0),
            grid_density=64,
            gravity = (0 , 0, 9.81),
            # visualize_mpm_boundary=True,
        ),
        viewer_options=gs.options.ViewerOptions(
            camera_pos=(3.5, 0.0, 2.5),
            camera_lookat=(0.0, 0.0, 0.5),
            camera_fov=40,
        ),

        show_viewer=args.vis,
    )

    ########################## entities ##########################
    frictionless_rigid = gs.materials.Rigid(needs_coup=True, coup_friction=0.0)

    # plane = scene.add_entity(
    #     material=frictionless_rigid,
    #     morph=gs.morphs.Plane(),
    # )
    
    cube = scene.add_entity(
        # material=frictionless_rigid,
        material=gs.materials.MPM.Elastic(rho = 30),
        morph=gs.morphs.Box(
            pos=(0.5, 0.5, 0.2),
            size=(0.2, 0.2, 0.2),
            euler=(30, 40, 0),
            fixed=True,
        ),
    )

    cloth = scene.add_entity(
        material=gs.materials.PBD.Cloth(),
        morph=gs.morphs.Mesh(
            file="meshes/cloth.obj",
            scale=1.0,
            pos=(0.5, 0.5, 0.5),
            euler=(180.0, 0.0, 0.0),
        ),
        surface=gs.surfaces.Default(
            color=(0.2, 0.4, 0.8, 1.0),
        ),
    )

    cam0 = scene.add_camera(
        pos = scene.viewer_options.camera_pos,
        lookat = scene.viewer_options.camera_lookat,
        fov = scene.viewer_options.camera_fov,
    )
    ########################## build ##########################
    scene.build()

    gs.tools.run_in_another_thread(
        fn = run_sim,
        args =[scene, cam0, args.vis]
    )
    if args.vis:
        scene.viewer.start()


if __name__ == "__main__":
    main()
