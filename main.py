from src.pipeline import (
    ground_filter, dtm, hydro, terrain, flow,
    flood, drainage, watershed
)

def main():
    ground_filter.run()
    dtm.run()
    hydro.run()
    terrain.run()
    flow.run()
    flood.run()
    drainage.run()
    watershed.run()

if __name__ == "__main__":
    main()