class_name Cookie
extends Sprite2D

func click():
	var player: AnimationPlayer = get_node("AnimationPlayer")
	player.play("pulse")

var timer = 0
func _process(delta):
	timer += delta
	if (timer > 5):
		timer = 0
		click()
