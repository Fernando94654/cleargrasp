import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

profile = pipeline.start(config)

color_stream = profile.get_stream(rs.stream.color)
intr = color_stream.as_video_stream_profile().get_intrinsics()

print("Width:", intr.width)
print("Height:", intr.height)
print("fx:", intr.fx)
print("fy:", intr.fy)
print("ppx (cx):", intr.ppx)
print("ppy (cy):", intr.ppy)

pipeline.stop()
