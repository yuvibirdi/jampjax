class_name Jack
extends Node

@onready
var player: AnimationPlayer = get_node("AnimationPlayer")

func pulse():
	player.play("pulse")
