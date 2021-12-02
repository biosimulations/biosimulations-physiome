from .core import getProjectsList, importProjects
import asyncio

def main():
    """
    Main function of the biosimulations-physiome package.
    """
    asyncio.run(importProjects())