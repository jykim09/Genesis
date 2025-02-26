import argparse

import numpy as np

import genesis as gs

def run_sim(scene, emitter1, emitter2, cam, enable_vis, recording) -> None:
    horizon = 600
    if recording:
        cam.start_recording()
    for i in range(horizon):
        if i < 400:
            emitter1.emit(
                pos=np.array([0.16, -0.4, 0.5]),
                direction=np.array([0.0, 0.0, -1.0]),
                speed=2,
                droplet_shape="circle",
                droplet_size=0.16,
            )
            emitter2.emit(
                pos=np.array([-0.16, -0.4, 0.5]),
                direction=np.array([0.0, 0.0, -1.0]),
                speed=3,
                droplet_shape="circle",
                droplet_size=0.16,
            )
        scene.step()
        cam.render()
        print(f'Current step : {i/horizon*100: .2f}%')
    if recording:
        cam.stop_recording(save_to_filename= 'flush.mp4')
    
    if enable_vis:
        scene.viewer.stop()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vis", action="store_true", default=False)
    parser.add_argument("-c", "--cpu", action="store_true", default=False)
    parser.add_argument("-r", "--rec", action="store_true", default=False)
    args = parser.parse_args()

    ########################## init ##########################
    gs.init(seed=0, precision="32", logging_level="debug", backend= gs.cpu if args.cpu else gs.gpu)

    ########################## create a scene ##########################

    scene = gs.Scene(
        sim_options=gs.options.SimOptions(
            dt=4e-3,
            substeps=20,
        ),
        mpm_options=gs.options.MPMOptions(
            lower_bound=(-0.45, -0.65, -0.01),
            upper_bound=(0.45, 0.65, 1.0),
            grid_density=64,
        ),
        viewer_options=gs.options.ViewerOptions(
            camera_pos=(4.5, 1.0, 1.42),
            camera_lookat=(0.0, 0.0, 0.3),
            camera_fov=22,
            max_FPS=120,
        ),
        show_viewer=args.vis,
        vis_options=gs.options.VisOptions(
            visualize_mpm_boundary=True,
        ),
    )

    # hanle camera
    cam = scene.add_camera(
        res = (640, 480),
        pos = scene.viewer_options.camera_pos,
        lookat= scene.viewer_options.camera_lookat,
        fov = scene.viewer_options.camera_fov,
    )

    ####### entity ###########################
    plane = scene.add_entity(morph=gs.morphs.Plane())
    cube0 = scene.add_entity(
        material=gs.materials.MPM.Elastic(rho=400),
        morph=gs.morphs.Box(
            pos=(0.0, 0.25, 0.4),
            size=(0.12, 0.12, 0.12),
        ),
        surface=gs.surfaces.Rough(
            color=(1.0, 0.5, 0.5, 1.0),
            vis_mode="particle",
        ),
    )

    cube0 = scene.add_entity(
        material=gs.materials.MPM.Elastic(rho=400),
        morph=gs.morphs.Sphere(
            pos=(0.15, 0.45, 0.5),
            radius=0.06,
        ),
        surface=gs.surfaces.Rough(
            color=(1.0, 1.0, 0.5, 1.0),
            vis_mode="particle",
        ),
    )

    cube0 = scene.add_entity(
        material=gs.materials.MPM.Elastic(rho=400),
        morph=gs.morphs.Cylinder(
            pos=(-0.15, 0.45, 0.6),
            radius=0.05,
            height=0.14,
        ),
        surface=gs.surfaces.Rough(
            color=(0.5, 1.0, 1.0, 1.0),
            vis_mode="particle",
        ),
    )
    emitter1 = scene.add_emitter(
        material=gs.materials.MPM.Liquid(sampler="random"),
        max_particles=80000,
        surface=gs.surfaces.Rough(
            color=(0.0, 0.9, 0.4, 1.0),
        ),
    )
    emitter2 = scene.add_emitter(
        material=gs.materials.MPM.Liquid(sampler="random"),
        max_particles=80000,
        surface=gs.surfaces.Rough(
            color=(0.0, 0.4, 0.9, 1.0),
        ),
    )

    scene.build()

    gs.tools.run_in_another_thread(
        fn = run_sim,
        args = (scene, emitter1, emitter2, cam, args.vis, args.rec)
    )

    if args.vis:
        scene.viewer.start()
    

if __name__ == "__main__":
    main()
