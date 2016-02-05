#!/usr/bin/env python3

import configparser

def main():
	config = configparser.ConfigParser()
	config.read('libraries.config')

	for library in config.sections():
		print(config.get(library,'name'), end = "")
		print(': ',end="")
		print(config.get(library,'gitURL'))

if __name__ == "__main__":
	main()
