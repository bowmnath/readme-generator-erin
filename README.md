Helpers to automatically generate markdown README for display on GitHub.

Once "installed" in your course repo,
you can update your `README.md` as follows:
* create a `base-readme.md` containing information that comes before the
  schedule (you need do this only once)
* update your `.readme-data.txt` as you want to modify your schedule
* commit
* push to GitHub

That's it!  The generation of the README from the data is handled by git hooks,
so you don't need to remember to do it manually.

# Installation

* Copy the `.helpers` directory to the base of your git repo.
* Copy the `pre-commit` file to the `.git/hooks/` directory in your repo as
  `.git/hooks/pre-commit`
* Copy the `pre-commit` file to the `.git/hooks/` directory in your repo as
  `.git/hooks/prepare-commit-msg`

At that point,
you are all set to start using the tool as described above.
The `.readme-data.txt` and `.base-readme.md` included in this repository are
just sample data.

If you are curious why `pre-commit` must be copied twice,
the explanation is in the `pre-commit` file itself.

# Format of README data

This is not a full description,
but hopefully it is reasonably simple to infer the format of the file from the
sample included in the repo.

In general,
the format of a line is
```
week, main text, link location, additional text
```
The link location and additional text are optional,
and either or both may be excluded.
If a link location is present,
the main text is rendered as a link to that location.

A few other notes of interest:
* blank lines do not matter
* any lines starting with `#` are ignored
* order of lines in the output is determined by their order in the input
* page breaks can be added to the slides (or any part) by adding a line that
  starts with the week number but is otherwise blank
* within the readings section, links cannot be inserted,
  and the text is instead rendered as-is

# Limitations

The format of `.readme-data.txt` was chosen because it made it simple to
duplicate the exact README I was using,
but the `generate_readme.py` script is not particularly flexible.
If you want your README to look different,
such as organization by day instead of week or having different columns or
putting single video links after each slide deck,
you will need to edit the Python source yourself.

There is currently no way to add anything below the schedule.
If you wanted to,
it would be trivial to make the `generate_readme.py` script look for a
`.post-readme.md` file or similar and append the contents to the end of the
generated README.

# Extra file

The `.helpers/check_capitalization.py` file has nothing to do with the rest
of the project and could be omitted.
If it is removed,
be sure also to remove the reference to it in `pre-commit`.
The file is included because I use it,
it seems unlikely to annoy most people,
and I doubt anyone will use this project in any case :)

# License

This code is released open-source under the MIT License.
