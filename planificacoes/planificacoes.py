from manim import *
import numpy as np

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_height = 8
config.frame_width = config.frame_height * config.pixel_width / config.pixel_height


# -----------------------------------------------------------
# 1. CUBO
# -----------------------------------------------------------
class PlanificacaoCubo(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=45 * DEGREES, zoom=0.8)
        
        base = Square(side_length=2, fill_opacity=0.8, fill_color=BLUE_E, stroke_color=WHITE)
        
        front = Square(side_length=2, fill_opacity=0.8, fill_color=RED_E, stroke_color=WHITE).next_to(base, DOWN, buff=0)
        top = Square(side_length=2, fill_opacity=0.8, fill_color=PURPLE_E, stroke_color=WHITE).next_to(front, DOWN, buff=0)
        back = Square(side_length=2, fill_opacity=0.8, fill_color=ORANGE, stroke_color=WHITE).next_to(base, UP, buff=0)
        left = Square(side_length=2, fill_opacity=0.8, fill_color=GREEN_E, stroke_color=WHITE).next_to(base, LEFT, buff=0)
        right = Square(side_length=2, fill_opacity=0.8, fill_color=YELLOW_E, stroke_color=WHITE).next_to(base, RIGHT, buff=0)

        unfolded_preview = VGroup(
            base.copy(), front.copy(), top.copy(), back.copy(), left.copy(), right.copy()
        )
        net_scale = min(
            1,
            (config.frame_width - 0.4) / unfolded_preview.width,
            (config.frame_height - 0.8) / unfolded_preview.height,
        )

        # Dobra a tampa (top) em relação à frente (front)
        top.rotate(PI/2, axis=np.cross(DOWN, [0,0,1]), about_point=front.get_bottom())
        front_group = VGroup(front, top)
        
        # Dobra todas as faces laterais para formar o cubo fechado
        front_group.rotate(PI/2, axis=np.cross(DOWN, [0,0,1]), about_point=base.get_bottom())
        back.rotate(PI/2, axis=np.cross(UP, [0,0,1]), about_point=base.get_top())
        left.rotate(PI/2, axis=np.cross(LEFT, [0,0,1]), about_point=base.get_left())
        right.rotate(PI/2, axis=np.cross(RIGHT, [0,0,1]), about_point=base.get_right())
        
        solid = VGroup(base, front_group, back, left, right)
        
        self.play(DrawBorderThenFill(solid))
        self.wait(1)
        
        # Animação de Planificação (Desdobrando)
        self.play(solid.animate.scale(net_scale), run_time=0.8)
        self.play(
            Rotate(front_group, -PI/2, axis=np.cross(DOWN, [0,0,1]), about_point=base.get_bottom()),
            Rotate(back, -PI/2, axis=np.cross(UP, [0,0,1]), about_point=base.get_top()),
            Rotate(left, -PI/2, axis=np.cross(LEFT, [0,0,1]), about_point=base.get_left()),
            Rotate(right, -PI/2, axis=np.cross(RIGHT, [0,0,1]), about_point=base.get_right()),
            run_time=2
        )
        self.play(
            Rotate(top, -PI/2, axis=np.cross(DOWN, [0,0,1]), about_point=front.get_bottom()),
            run_time=1.5
        )
        self.wait(1)
        
        # Câmera visualiza de cima
        self.move_camera(phi=0, theta=-90 * DEGREES, run_time=2)
        self.wait(2)


# -----------------------------------------------------------
# FUNÇÃO GERADORA DE PIRÂMIDES (Lógica Universal de Dobradura)
# -----------------------------------------------------------
def create_pyramid_scene(scene, N, radius, height, color):
    scene.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES, zoom=0.8)
    
    base = RegularPolygon(n=N, radius=radius, fill_opacity=0.8, fill_color=color, stroke_color=WHITE)
    vertices = base.get_vertices()
    
    d = radius * np.cos(PI/N)
    s = np.sqrt(d**2 + height**2)
    fold_angle = PI - np.arccos(d/s)
    
    faces = VGroup()
    fold_axes = []
    
    for i in range(N):
        v1 = vertices[i]
        v2 = vertices[(i+1)%N]
        edge_center = (v1 + v2) / 2
        
        direction = edge_center / np.linalg.norm(edge_center)
        apex_2d = edge_center + direction * s
        
        face = Polygon(v1, v2, apex_2d, fill_opacity=0.8, fill_color=color, stroke_color=WHITE)
        fold_axis = np.cross(direction, [0,0,1])
        
        faces.add(face)
        fold_axes.append(fold_axis)

    unfolded_preview = VGroup(base.copy(), faces.copy())
    net_scale = min(
        1,
        (config.frame_width - 0.4) / unfolded_preview.width,
        (config.frame_height - 0.8) / unfolded_preview.height,
    )

    for face, axis, i in zip(faces, fold_axes, range(N)):
        edge_center = (vertices[i] + vertices[(i + 1) % N]) / 2
        face.rotate(fold_angle, axis=axis, about_point=edge_center)
        
    solid = VGroup(base, faces)
    
    scene.play(DrawBorderThenFill(solid))
    scene.wait(1)
    
    # Anima a planificação
    scene.play(solid.animate.scale(net_scale), run_time=0.8)
    vertices = base.get_vertices()
    anims_unfold = [
        Rotate(
            face,
            -fold_angle,
            axis=axis,
            about_point=(vertices[i] + vertices[(i + 1) % N]) / 2,
        )
        for i, (face, axis) in enumerate(zip(faces, fold_axes))
    ]
    scene.play(*anims_unfold, run_time=2)
    scene.wait(1)
    
    scene.move_camera(phi=0, theta=-90*DEGREES, run_time=2)
    scene.wait(2)


# -----------------------------------------------------------
# 2. TETRAEDRO (Pirâmide Triangular)
# -----------------------------------------------------------
class PlanificacaoTetraedro(ThreeDScene):
    def construct(self):
        create_pyramid_scene(self, 3, 2.5, 2.5 * np.sqrt(2), GREEN_E)

# -----------------------------------------------------------
# 3. PIRÂMIDE DE BASE QUADRADA
# -----------------------------------------------------------
class PlanificacaoPiramideQuadrada(ThreeDScene):
    def construct(self):
        create_pyramid_scene(self, 4, 2, 2.5, RED_E)

# -----------------------------------------------------------
# 4. PIRÂMIDE DE BASE HEXAGONAL
# -----------------------------------------------------------
class PlanificacaoPiramideHexagonal(ThreeDScene):
    def construct(self):
        create_pyramid_scene(self, 6, 2, 3, MAROON_E)


# -----------------------------------------------------------
# 5. CILINDRO (Abertura paramétrica curva)
# -----------------------------------------------------------
class PlanificacaoCilindro(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=45 * DEGREES, zoom=0.8)
        
        tracker = ValueTracker(1) # 1 = Cilindro Fechado, 0 = Planificado
        scale_tracker = ValueTracker(1)
        R = 1.5
        H = 4
        net_scale = min(
            1,
            (config.frame_width - 0.4) / (2 * PI * R),
            (config.frame_height - 0.8) / (H + 2 * R),
        )
        
        def cylinder_func(u, v):
            t = tracker.get_value()
            if t < 0.001:
                x = (u - 0.5) * 2 * PI * R
                y = (v - 0.5) * H
                z = -R
                return np.array([x, y, z]) * scale_tracker.get_value()
            else:
                r = R / t
                theta = (u - 0.5) * 2 * PI * t
                x = r * np.sin(theta)
                y = (v - 0.5) * H
                z = -R + r - r * np.cos(theta)
                return np.array([x, y, z]) * scale_tracker.get_value()
                
        surface = always_redraw(lambda: Surface(
            cylinder_func,
            u_range=[0, 1], v_range=[0, 1],
            resolution=(32, 1),
            fill_color=TEAL_E, fill_opacity=0.8, stroke_width=0
        ))
        
        def top_cap_pos():
            t = tracker.get_value()
            scale = scale_tracker.get_value()
            circle = Circle(radius=R * scale, fill_color=TEAL_E, fill_opacity=0.8, stroke_color=WHITE)
            circle.shift(scale * (UP * (H/2 + R) + IN * R))
            circle.rotate(PI/2 * t, axis=RIGHT, about_point=scale * np.array([0, H/2, -R]))
            return circle

        def bot_cap_pos():
            t = tracker.get_value()
            scale = scale_tracker.get_value()
            circle = Circle(radius=R * scale, fill_color=TEAL_E, fill_opacity=0.8, stroke_color=WHITE)
            circle.shift(scale * (DOWN * (H/2 + R) + IN * R))
            circle.rotate(-PI/2 * t, axis=RIGHT, about_point=scale * np.array([0, -H/2, -R]))
            return circle
            
        top_cap = always_redraw(top_cap_pos)
        bot_cap = always_redraw(bot_cap_pos)
        
        self.play(FadeIn(surface), FadeIn(top_cap), FadeIn(bot_cap))
        self.wait(1)
        
        # Desdobrando o cilindro
        self.play(tracker.animate.set_value(0), run_time=3)
        self.wait(1)
        self.play(scale_tracker.animate.set_value(net_scale), run_time=1)
        
        self.move_camera(phi=0, theta=-90*DEGREES, run_time=2)
        self.wait(2)


# -----------------------------------------------------------
# 6. CONE (Transformação Morfológica 3D -> 2D)
# -----------------------------------------------------------
class PlanificacaoCone(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=45 * DEGREES, zoom=0.8)
        
        R = 1.5
        H = 3.5
        s = np.sqrt(R**2 + H**2)
        alpha = 2 * PI * R / s
        
        # Sólido 3D
        cone = Cone(base_radius=R, height=H, direction=OUT, fill_color=PURPLE_E, fill_opacity=0.8)
        cone.shift(OUT * H/2)
        base_cap_3d = Circle(radius=R, fill_color=PURPLE_E, fill_opacity=0.8).shift(IN * H/2)
        solid = VGroup(cone, base_cap_3d)
        
        # Planificação 2D (Setor Circular + Círculo da Base)
        sector = Sector(radius=s, angle=alpha, start_angle=-PI/2 - alpha/2, fill_color=PURPLE_E, fill_opacity=0.8, stroke_color=WHITE)
        sector.shift(UP * 1.5)
        
        base_cap_2d = Circle(radius=R, fill_color=PURPLE_E, fill_opacity=0.8, stroke_color=WHITE)
        base_cap_2d.next_to(sector, DOWN, buff=0)
        net = VGroup(sector, base_cap_2d)
        net_scale = min(
            (config.frame_width - 0.4) / net.width,
            (config.frame_height - 0.8) / net.height,
        )
        net.scale(net_scale).move_to(ORIGIN)
        
        self.play(DrawBorderThenFill(solid))
        self.wait(1)
        
        self.move_camera(phi=0, theta=-90*DEGREES, run_time=2.5)
        # Transição suave desenrolando o cone no plano 2D
        self.play(ReplacementTransform(solid, net), run_time=2.5)
        self.wait(2)