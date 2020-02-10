import myadventure
import pyzork

adventure = pyzork.CustomAdventure()

adventure.set_classes(myadventure.classes.list_of_classes)
adventure.set_map(myadventure.map.WorldMap)

adventure


if __name__ == '__main__':
    adventure.start()
