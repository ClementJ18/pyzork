.. pyzork documentation master file, created by
   sphinx-quickstart on Tue Feb 18 21:20:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
   
.. currentmodule:: pyzork

Welcome to pyzork's documentation!
==================================
.. image:: https://readthedocs.org/projects/pyzork/badge/?version=latest
   :target: https://pyzork.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: Licence: MIT

.. image:: https://img.shields.io/github/issues/ClementJ18/pyzork.svg
   :target: https://github.com/ClementJ18/pyzork/issues
   :alt: Open Issues

.. image:: https://img.shields.io/github/issues-pr/ClementJ18/pyzork.svg
   :target: https://github.com/ClementJ18/pyzork/pulls
   :alt: Open PRs

.. image:: https://img.shields.io/github/stars/ClementJ18/pyzork.svg?label=Stars&style=social 
   :target: https://github.com/ClementJ18/pyzork
   :alt: Stars

pyzork is a python library to make creating text adventures easier. The usual steps to creating anything using this library is to subclass the parent of the thing you want to create. For example, if you want to create a Goblin for your player to fight you'll need to subclass :class:`pyzork.entities.NPC`. If you want to create a Tavern for your players to visit you'll need to subclass :class:`pyzork.world.Location` and so on. Each class and method has documentation including examples so it's just a matter of finding it. 

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   started
   entities
   modifiers
   abilities
   levels
   base
   battle
   world
   parsers
   equipment
   visualise
   hints
   sample
   enums
   errors
