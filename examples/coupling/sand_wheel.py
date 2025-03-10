import argparse

import numpy as np

import genesis as gs

def run_sim(scene, emitter, cam, enable_vis, recording):
    if recording:
        cam.start_recording()
    
    horizon = 1000
    for i in range(horizon):
        print(f'Current step : {i/horizon*100: .2f}%')
        emitter.emit(
            pos=np.array([0.5, 0.0, 2.3]),
            direction=np.array([0.0, np.sin(i / 10) * 0.35, -1.0]),
            speed=8.0,
            droplet_shape="rectangle",
            droplet_size=[0.03, 0.05],
        )
        scene.step()
        cam.render()

    if recording:
        cam.stop_recording(save_to_filename = "sand_wheel.mp4")

    if enable_vis:
        scene.viewer.stop()
    


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vis", action="store_true", default=False)
    parser.add_argument("-c", "--cpu", action="store_true", default=False)
    parser.add_argument("-r", "--rec", action="store_true", default=False)
    
    args = parser.parse_args()

    ########################## init ##########################
    gs.init(seed=0, precision="32", logging_level="debug", backend= gs.cpu if args.cpu else gs.metal)

    ########################## create a scene ##########################
    scene = gs.Scene(
        sim_options=gs.options.SimOptions(
            dt=3e-3,
            substeps=10,
        ),
        mpm_options=gs.options.MPMOptions(
            lower_bound=(0.0, -1.0, -0.1),
            upper_bound=(0.57, 1.0, 2.4),
            grid_density=64,
        ),
        show_viewer=args.vis,
        viewer_options=gs.options.ViewerOptions(
            camera_pos=(4.5, 0.0, 1.42),
            camera_lookat=(1.0, 0.0, 1.0),
            camera_fov=30,
            max_FPS=120,
        ),
        vis_options=gs.options.VisOptions(
            visualize_mpm_boundary=True,
        ),
    )
    # camera handle

    cam0 = scene.add_camera(
        res = (640,480),
        pos = scene.viewer_options.camera_pos,
        lookat = scene.viewer_options.camera_lookat,
        fov = scene.viewer_options.camera_fov,
    )

    plane = scene.add_entity(
        material=gs.materials.Rigid(
            needs_coup=True,
            coup_friction=0.2,
        ),
        morph=gs.morphs.URDF(file="urdf/plane/plane.urdf", fixed=True),
    )
    mat_wheel = gs.materials.Rigid(
        needs_coup=True,
        coup_softness=0.0,
    )
    wheel_0 = scene.add_entity(
        material=mat_wheel,
        morph=gs.morphs.URDF(
            file="urdf/wheel/wheel.urdf",
            pos=(0.5, -0.2, 1.6),
            euler=(0, 0, 90),
            scale=0.6,
            convexify=False,
            fixed=True,
        ),
    )

    wheel_0 = scene.add_entity(
        material=mat_wheel,
        morph=gs.morphs.URDF(
            file="urdf/wheel/wheel.urdf",
            pos=(0.5, 0.3, 1.2),
            euler=(0, 0, 90),
            scale=0.6,
            convexify=False,
            fixed=True,
        ),
    )

    wheel_0 = scene.add_entity(
        material=mat_wheel,
        morph=gs.morphs.URDF(
            file="urdf/wheel/wheel.urdf",
            pos=(0.5, -0.3, 0.8),
            euler=(0, 0, 90),
            scale=0.6,
            convexify=False,
            fixed=True,
        ),
    )

    wheel_0 = scene.add_entity(
        material=mat_wheel,
        morph=gs.morphs.URDF(
            file="urdf/wheel/wheel.urdf",
            pos=(0.5, 0.4, 0.4),
            euler=(0, 0, 90),
            scale=0.6,
            convexify=False,
            fixed=True,
        ),
    )

    emitter = scene.add_emitter(
        material=gs.materials.MPM.Sand(),
        max_particles=200000,
        surface=gs.surfaces.Rough(
            color=(1.0, 0.9, 0.6, 1.0),
        ),
    )
    scene.build()

    gs.tools.run_in_another_thread(
        fn = run_sim,
        args = (scene, emitter, cam0, args.vis, args.rec)
    )

    scene.viewer.start()

if __name__ == "__main__":
    main()
