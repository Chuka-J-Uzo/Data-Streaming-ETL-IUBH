import android

droid = android.Android()

while True:
    values = droid.sensorsReadGyroscope().result
    x, y, z = values['x'], values['y'], values['z']
    print(f"Gyroscope values: x={x}, y={y}, z={z}")
