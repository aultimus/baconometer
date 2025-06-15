import csv

NAME_BASICS_PATH = "name.basics.tsv"
TITLE_BASICS_PATH = "title.basics.tsv"
ACTORS_CSV = "actors.csv"
FILMS_CSV = "films.csv"
ACTED_IN_CSV = "acted_in.csv"


def count_lines(path):
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in f) - 1  # subtract header


def main():
    print("Counting total films and actors...")
    total_films = count_lines(TITLE_BASICS_PATH)
    total_actors = count_lines(NAME_BASICS_PATH)
    print(f"Total films: {total_films}, total actors: {total_actors}")
    print("Generating films.csv...")
    film_ids = set()
    with open(TITLE_BASICS_PATH, encoding="utf-8") as infile, open(
        FILMS_CSV, "w", newline="", encoding="utf-8"
    ) as outfile:
        reader = csv.DictReader(infile, delimiter="\t")
        writer = csv.writer(outfile)
        writer.writerow(["tconst:ID(Film)", "title"])
        i = 0
        for row in reader:
            film_ids.add(row["tconst"])
            writer.writerow([row["tconst"], row["primaryTitle"]])
            i += 1
            if i % 10000 == 0:
                print(f"Processed {i}/{total_films} films ({i*100//total_films}%)")
    print(f"Done. Wrote {i} films.")

    print("Generating actors.csv and acted_in.csv...")
    with open(NAME_BASICS_PATH, encoding="utf-8") as infile, open(
        ACTORS_CSV, "w", newline="", encoding="utf-8"
    ) as actors_out, open(
        ACTED_IN_CSV, "w", newline="", encoding="utf-8"
    ) as acted_in_out:
        reader = csv.DictReader(infile, delimiter="\t")
        actors_writer = csv.writer(actors_out)
        acted_in_writer = csv.writer(acted_in_out)
        actors_writer.writerow(["nconst:ID(Actor)", "name"])
        acted_in_writer.writerow([":START_ID(Actor)", ":END_ID(Film)"])
        i = 0
        rels = 0
        for row in reader:
            actors_writer.writerow([row["nconst"], row["primaryName"]])
            if row["knownForTitles"]:
                for title_id in row["knownForTitles"].split(","):
                    if title_id in film_ids:
                        acted_in_writer.writerow([row["nconst"], title_id])
                        rels += 1
            i += 1
            if i % 10000 == 0:
                print(
                    f"Processed {i}/{total_actors} actors ({i*100//total_actors}%), {rels} relationships written"
                )
    print(f"Done. Wrote {i} actors and {rels} relationships.")


if __name__ == "__main__":
    main()
