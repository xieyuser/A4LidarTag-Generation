#! /usr/bin/env python
import os
import os.path as osp
import json

import numpy as np
import click

import svgwrite
from svgwrite import cm, mm
import cairosvg


def add_rect(dwg, x, y, w, h, color):
    print(x, y, w, h, color)
    rec = dwg.rect(insert=(x * cm, y * cm), size=(w * cm, h  * cm), fill=color, stroke=color)
    return rec

def add_circle(dwg, x, y, r, color):
    print(x, y, r)
    circle = dwg.circle(center=(x* cm, y * cm), r=f'{r}cm', fill=color)
    return circle

def generate_pattern_aruco(dwg, r, code):
    print(code)
    width = 20
    ul = [0.12*width, 0.3*width]
    x, y = code[0][0]
    print(x, y)
    x_bytes, y_bytes = bin(x)[2:].rjust(8, '0'), bin(y)[2:].rjust(8, '0')
    bytess = [int(b) for b in x_bytes + y_bytes]
    bytess = np.asarray(bytess).reshape((4, 4)).tolist()
    print(bytess)
    for i in range(4):
        for j in range(4):
            if bytess[i][j] == 1:
                dwg.add(add_circle(dwg, ul[0]+j * 0.25*width, ul[1] + i*0.25*width, r, 'black'))
            else:
                continue
    dwg.save()
    return dwg

@click.command()
@click.option("--out", "save_dir", default='./out')
@click.option("--width", default=20)
@click.option("--count", type=click.INT, default=4)
@click.option("--json-path", default='./config/dict.json')
@click.option("--pdf", "pdf_dir", default='./pdf')
def cli(save_dir, width, count, json_path, pdf_dir):
    height = width * 1.5
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)

    with open(json_path, 'r') as f:
        aruco_dec = json.load(f)
        nums = len(aruco_dec)

    for id_index, id in enumerate(range(nums)):
        path = osp.join(save_dir, f'{id}.svg')
        dwg = svgwrite.Drawing(filename=path, size=(width * cm, height * cm), debug=True)

        # lidartag
        aruco_r = 0.04 * width

        dwg = generate_pattern_aruco(dwg, aruco_r, aruco_dec[str(id_index)])

        # to pdf
        if pdf_dir:
            cairosvg.svg2pdf(file_obj=open(path, "rb"), write_to=osp.join(pdf_dir, path.split("/")[-1].replace('.svg', '.pdf')))

if __name__ == '__main__':
    cli()

