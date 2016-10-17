adb shell screencap /sdcard/mytmp/rock.raw
adb pull /sdcard/mytmp/rock.raw
adb shell rm /sdcard/mytmp/rock.raw

// remove the header
tail -c +13 rock.raw > rock.rgba

// extract width height and pixelformat:
hexdump -e '/4 "%d"' -s 0 -n 4 rock.raw
hexdump -e '/4 "%d"' -s 4 -n 4 rock.raw
hexdump -e '/4 "%d"' -s 8 -n 4 rock.raw

convert -size 480x800 -depth 8 rock.rgba rock.png
