import argparse

import genesis as gs

def run_sim(scene,enable_vis):
    for i in range(800):
        scene.step()
    if enable_vis:
        scene.viewer.stop()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vis", action="store_true", default=False)
    args = parser.parse_args()

    ########################## init ##########################
    gs.init(seed=0, precision="32", logging_level="debug", backend= gs.metal)

    ########################## create a scene ##########################

    scene = gs.Scene(
        sim_options=gs.options.SimOptions(
            dt = 2e-3,
            substeps=10,
            gravity = (0, 0, -9.81),
        ),
        vis_options=gs.options.VisOptions(
            visualize_sph_boundary=True,
            visualize_mpm_boundary=True,
        ),
        mpm_options=gs.options.MPMOptions(
            lower_bound=(0.0, 0.0, -0.1),
            upper_bound=(1.0, 1.0, 1.0),
        ),
        sph_options=gs.options.SPHOptions(
            lower_bound=(-0.03, -0.03, -0.08),
            upper_bound=(1.03, 1.03, 1.0),
        ),
        viewer_options=gs.options.ViewerOptions(
            camera_pos=(0.8, -3, 1.42),
            camera_lookat=(0.5, 0.5, 0.4),
            camera_fov=30,
            max_FPS=60,
        ),
        show_viewer=True,
    )

    ########################## entities ##########################

    water = scene.add_entity(
        material=gs.materials.SPH.Liquid(),
        morph=gs.morphs.Box(
            pos=(0.4, 0.5, 0.25),
            size=(0.7, 0.9, 0.5),
        ),
        surface=gs.surfaces.Default(
            color=(0.2, 0.6, 1.0, 1.0),
            vis_mode="particle",
        ),
    )

    duck = scene.add_entity(
        material=gs.materials.MPM.Elastic(rho=200),
        morph=gs.morphs.Mesh(
            file="meshes/duck.obj",
            pos=(0.5, 0.5, 0.7),
            scale=0.07,
            euler=(90.0, 0.0, 90.0),
        ),
        surface=gs.surfaces.Default(
            color=(0.9, 0.8, 0.2, 1.0),
            vis_mode="particle",
        ),
    )
    ### mac에서는 plane을 추가하는 것때문에 gpu을 사용하지 못했음.
    ### 이 부분을 제거하고 실행하면 사용에 문제가 없음.
    ### taichi가 사용될 경우 문제가 발생함을 확인할 수 있음.
    plane = scene.add_entity(
        morph=gs.morphs.Plane(
        pos=(0.0, 0.0, -5),  # 기존보다 낮은 위치로 변경
        normal=(0, 0, 1),  # 노멀 방향 지정
        ),
    )
    ########################## build ##########################
    scene.build()




    gs.tools.run_in_another_thread(
        fn = run_sim,
        args= (scene,True)
    )

    scene.viewer.start()


if __name__ == "__main__":
    main()
