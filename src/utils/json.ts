// Utilities related with json files.

import fs from "fs";

/**
 * Reads and parses a json file.
 * 
 * @param path The path to the file considering the current repository as root.
 * @returns A list with the list from the json file.
 */
export function loadJsonFile (
    path: string
): Array<string> {
    const appRoot = require("app-root-path");
    try {
        const data = fs.readFileSync(
            `${appRoot}${path[0] === "/" ? path : "/" + path}`
        );
        return JSON.parse(data as any);
    } catch (err) {
        throw Error(
            `loadJsonFile: ${err}`
        );
    }
}

/**
 * Exports data to a json file.
 * 
 * @param data The array to be exported
 * @param path The path to the file considering the current repository as root.
 * @param mode If either to append or write a clean file.
 *  Use `a` for append and `w` for write. Defaults to `w`.
 */
export function writeJsonFile (
    data: Array<string>,
    path: string,
    mode?: string
) {
    try {
        const appRoot = require("app-root-path");
        let prevData: Array<string>;
        let resolvedMode = mode === undefined ? "a" : mode;

        if (resolvedMode === "a") {
            prevData = loadJsonFile(path);
        } else if (resolvedMode === "w") {
            prevData = []
        } else {
            throw Error(`Invalid mode: ${resolvedMode}`);
        }

        const outputData = JSON.stringify(
            prevData.push(...data),
            null,
            2
        );
        
        const outputPath = `${appRoot}${path[0] === "/" ? path : "/" + path}`;
        fs.writeFileSync(
            outputPath,
            outputData
        );
        console.log(
            `File written to: ${outputPath}`
        );
    } catch (err) {
        throw Error(
            `writeJsonFile: ${err}`
        );
    }
}
