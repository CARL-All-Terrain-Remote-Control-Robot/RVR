import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
sys.path.insert(1,"../../include/sphero-sdk-raspberrypi-python")
import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import Colors
from sphero_sdk import RvrLedGroups
from sphero_sdk import SerialAsyncDal
from sphero_sdk import SpheroRvrTargets


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)

async def main():
    """ This program demonstrates how to set multiple LEDs.
    """

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)
    print("starting echo")
    echo_response = await rvr.echo(
        data=[0, 1, 2],
        target=SpheroRvrTargets.primary.value
    )
    print('Echo response 1: ', echo_response)

    await rvr.set_all_leds(
        led_group=RvrLedGroups.all_lights.value,
        led_brightness_values=[color for _ in range(10) for color in Colors.off.value]
    )

    # Delay to show LEDs change
    await asyncio.sleep(10)

    await rvr.set_all_leds(
        led_group=RvrLedGroups.headlight_left.value | RvrLedGroups.headlight_right.value,
        led_brightness_values=[
            0, 0, 255,
            255, 0, 0
        ]
    )

    # Delay to show LEDs change
    await asyncio.sleep(10)

    await rvr.close()


if __name__ == '__main__':
    try:
        print("Iran")
        loop.run_until_complete(

            main()
        )

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

        loop.run_until_complete(
            rvr.close()
        )

    finally:
        if loop.is_running():
            loop.close()
