/**
 * Advent of Code 2023
 * Day 14: Parabolic Reflector Dish
 * Part 2
 * 
 * @auhor Daniel Herding
 */
 
import java.io.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;

import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import java.util.stream.*;

public class Adv14b {

    private static String toString(List<List<Boolean>> landscape) {
        StringBuilder builder = new StringBuilder();
        for (List<Boolean> line: landscape) {
            for (Boolean pos: line) {
                if (pos == null) {
                    builder.append(".");
                } else if (pos) {
                    builder.append("O");
                } else {
                    builder.append("#");
                }
            }
            builder.append("\n");
        }
        // Remove last newline
        builder.deleteCharAt(builder.length() - 1);
        
        return builder.toString();
    }

    private static List<List<Boolean>> fromString(String landscapeStr) {
        List<String> lines = Arrays.asList(landscapeStr.split("\n"));
        List<List<Boolean>> landscape = new ArrayList<>();
        for (int y = 0; y < lines.size(); y++) {
            List<Boolean> line = new ArrayList<>();
            for (int x = 0; x < lines.get(y).length(); x++) {
                char c = lines.get(y).charAt(x);
                if (c == '#') {
                    line.add(Boolean.FALSE);
                } else if (c == 'O') {
                    line.add(Boolean.TRUE);
                } else if (c == '.') {
                    line.add(null);
                }
            }
            landscape.add(line);
        }
        return landscape;
    }

    private static Map<String, String> CACHE = new HashMap<>();

    private static int calculateLoad(String landscapeStr) {
        List<List<Boolean>> landscape = fromString(landscapeStr);
        int result = 0;
        for (int y = 0; y < landscape.size(); y++) {
            List<Boolean> row = landscape.get(y);
            for (Boolean b: row) {
                if (b == Boolean.TRUE) {
                    result += landscape.size() - y;
                }
            }
        }
        return result;
    }
    
    private static String cycle(String landscapeStr) {
        String cachedResult = CACHE.get(landscapeStr);
        if (cachedResult != null) {
            return cachedResult;
        }
        
        List<List<Boolean>> newLandscape = fromString(landscapeStr);

        // Roll north
        for (int rep = 0; rep < newLandscape.size() - 1; rep++) {
            for (int y = 0; y < newLandscape.size() - 1; y++) {
                for (int x = 0; x < newLandscape.get(y).size(); x++) {
                    if (newLandscape.get(y).get(x) == null && newLandscape.get(y + 1).get(x) == Boolean.TRUE) {
                        newLandscape.get(y).set(x, Boolean.TRUE);
                        newLandscape.get(y + 1).set(x, null);
                    }
                }
            }
        }
        
        // Roll west
        for (int rep = 0; rep < newLandscape.get(0).size() - 1; rep++) {
            for (int y = 0; y < newLandscape.size(); y++) {
                for (int x = 0; x < newLandscape.get(y).size() - 1; x++) {
                    if (newLandscape.get(y).get(x) == null && newLandscape.get(y).get(x + 1) == Boolean.TRUE) {
                        newLandscape.get(y).set(x, Boolean.TRUE);
                        newLandscape.get(y).set(x + 1, null);
                    }
                }
            }
        }

        // Roll south
        for (int rep = 0; rep < newLandscape.size() - 1; rep++) {
            for (int y = 0; y < newLandscape.size() - 1; y++) {
                for (int x = 0; x < newLandscape.get(y).size(); x++) {
                    if (newLandscape.get(y).get(x) == Boolean.TRUE && newLandscape.get(y + 1).get(x) == null) {
                        newLandscape.get(y).set(x, null);
                        newLandscape.get(y + 1).set(x, Boolean.TRUE);
                    }
                }
            }
        }

        // Roll east
        for (int rep = 0; rep < newLandscape.get(0).size() - 1; rep++) {
            for (int y = 0; y < newLandscape.size(); y++) {
                for (int x = 0; x < newLandscape.get(y).size() - 1; x++) {
                    if (newLandscape.get(y).get(x) == Boolean.TRUE && newLandscape.get(y).get(x + 1) == null) {
                        newLandscape.get(y).set(x, null);
                        newLandscape.get(y).set(x + 1, Boolean.TRUE);
                    }
                }
            }
        }
        
        String newLandscapeStr = toString(newLandscape);
        CACHE.put(landscapeStr, newLandscapeStr);
        return newLandscapeStr;
    }

    public static void main(String[] args) throws IOException {
        String landscapeStr = Files.readString(Paths.get("14.txt"), StandardCharsets.UTF_8);
        //System.out.println(landscapeStr);
        
        for (long cyc = 0; cyc < 1000000000; cyc++) {
            landscapeStr = cycle(landscapeStr);
        }
        
        System.out.println("Part 2 result: " + calculateLoad(landscapeStr));
    }
}
