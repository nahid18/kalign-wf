"""
Fast Multiple Sequence Alignment 
"""
from datetime import datetime
from pathlib import Path
import subprocess
import os

from latch import small_task, workflow, message
from latch.resources.launch_plan import LaunchPlan
from latch.types import LatchAuthor, LatchFile, LatchMetadata, LatchParameter, LatchDir



@small_task
def kalign_task(
    seqs: LatchFile,
    gpo: int,
    gpe: int,
    tgpe: int,
) -> LatchDir:
    def get_timestamp():
        format_str = "%d %b %Y %H:%M:%S %p"
        result = datetime.now().strftime(format_str)
        return result
    
    curr_timestamp = "".join([x if x.isalnum() else "_" for x in get_timestamp()])
    out_dir = f"kalign_{curr_timestamp}"
    os.system(command=f"mkdir -p {out_dir}")
    message("info", {"title": f"Output Directory: {out_dir}", "body": f"Output will be saved to {out_dir} directory."})
    
    os.system(command=f"kalign --version > {out_dir}/version.txt")
    
    return LatchDir(path=str(out_dir), remote_path=f"latch:///{out_dir}/")


"""The metadata included here will be injected into your interface."""
metadata = LatchMetadata(
    display_name="Kalign",
    documentation="https://github.com/TimoLassmann/kalign#readme",
    author=LatchAuthor(
        name="Abdullah Al Nahid",
        email="abdnahid56@gmail.com",
        github="github.com/nahid18",
    ),
    repository="",
    license="MIT",
    parameters={
        "seqs": LatchParameter(
            display_name="Input Fasta",
            description="Concatenated fasta file containing all the sequences to be aligned",
            batch_table_column=False,
        ),
        "gpo": LatchParameter(
            display_name="Gap Open Penalty",
            description="Gap Open Penalty",
            batch_table_column=False,
        ),
        "gpe": LatchParameter(
            display_name="Gap Extension Penalty",
            description="Gap Extension Penalty",
            batch_table_column=False,
        ),
        "tgpe": LatchParameter(
            display_name="Terminal Gap Penalties",
            description="Terminal Gap Penalties",
            batch_table_column=False,
        )
    },
)


@workflow(metadata)
def kalign(
    seqs: LatchFile,
    gpo: int = 11,
    gpe: int = 4,
    tgpe: int = 2,
) -> LatchDir:
    """A fast multiple sequence alignment program

    Kalign
    ----
    [Kalign](https://github.com/TimoLassmann/kalign) is a fast multiple sequence alignment program for biological sequences.

    ## Input Options
    1. **Required**: A concatenated `fasta file` containing all the sequences to be aligned.
    2. *Optional*: `output format`, `gap open penalty`, `gap extension penalty` and `terminal gap penalties`.

    ## Please cite:
    1. Lassmann, Timo. _Kalign 3: multiple sequence alignment of large data sets._ **Bioinformatics** (2019). [pdf](https://academic.oup.com/bioinformatics/advance-article-pdf/doi/10.1093/bioinformatics/btz795/30314127/btz795.pdf)
    """
    return kalign_task(seqs=seqs, gpo=gpo, gpe=gpe, tgpe=tgpe)


# Test Data
LaunchPlan(
    kalign,
    "Test Data",
    {
        "seqs": LatchFile("s3://latch-public/test-data/3729/kalign_data.fasta"),
        "gpo": 11,
        "gpe": 4,
        "tgpe": 2,
    },
)
