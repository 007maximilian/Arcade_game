import arcade
from arcade.particles import Emitter, FadeParticle, EmitBurst, EmitInterval, EmitMaintainCount
import random

SPARK_TEX = [
    arcade.make_soft_circle_texture(8, arcade.color.PASTEL_YELLOW),
    arcade.make_soft_circle_texture(8, arcade.color.PEACH),
    arcade.make_soft_circle_texture(8, arcade.color.BABY_BLUE),
    arcade.make_soft_circle_texture(8, arcade.color.ELECTRIC_CRIMSON),
]
SMOKE_TEX = arcade.make_soft_circle_texture(20, arcade.color.LIGHT_GRAY, 255, 80)
PUFF_TEX = arcade.make_soft_circle_texture(12, arcade.color.WHITE, 255, 50)


def gravity_drag(p):
    p.change_y += -0.03
    p.change_x *= 0.92
    p.change_y *= 0.92


def make_ring(x, y, count=40, radius=5.0):
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(count),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=arcade.make_soft_circle_texture(60, arcade.color.RED),
            change_xy=arcade.math.rand_on_circle((0.0, 0.0), radius),
            lifetime=random.uniform(0.8, 1.4),
            start_alpha=255, end_alpha=0,
            scale=random.uniform(0.4, 0.7),
            mutation_callback=gravity_drag,
        ),
    )