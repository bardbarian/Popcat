import sys
import popcat

if __name__ == "__main__":
    python_version = ".".join([str(num) for num in sys.version_info[0:3]])

    if sys.version_info[0] != 3 or sys.version_info[1] < 6:
        print(f"Popcat requires Python 3.6+.\nYou are currently using Python {python_version}.")
        sys.exit(1)

    popcat.main()