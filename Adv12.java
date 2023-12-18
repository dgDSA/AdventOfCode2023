
/**
 * Advent of Code 2023
 * Day 12: Hot Springs (not as elegant as the Python solution)
 * 
 * @auhor Daniel Herding
 */

import java.io.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.Pattern;
import java.util.stream.Collector;
import java.util.stream.Collectors;

public class Adv12 {

    private static Pattern R_WORKING = Pattern.compile("(\\.+).*");

    private static Map<Short, Pattern> R_POSSIBLY_BROKEN = new HashMap<>();
    static {
        for (short i = 0; i <= 16; i++) {
            R_POSSIBLY_BROKEN.put(i, Pattern.compile("([\\#\\?]{" + i + "}(\\.+|\\?|$))"));
        }
    }

    // Nearly the same as above, but also matches the rest of the line.
    // Damn. If Java's Matcher.matches() is like Python's re.fullmatch(),
    // Then what is Java's equivalent of Python's re.match()?
    private static Map<Short, Pattern> R_POSSIBLY_BROKEN_FULL = new HashMap<>();
    static {
        for (short i = 0; i <= 16; i++) {
            R_POSSIBLY_BROKEN_FULL.put(i, Pattern.compile("([\\#\\?]{" + i + "}(\\.+|\\?|$)).*"));
        }
    }

    private Map<String, Long> cache = new HashMap<>();

    private long findArrangements(String row, List<Short> damagedList) {
        String cacheKey = row + damagedList;
        if (cache.containsKey(cacheKey)) {
            return cache.get(cacheKey);
        }
        long result;
        if (row.isEmpty()) {
            if (damagedList.isEmpty()) {
                // Arrangement found
                result = 1;
            } else {
                // Fail: reached end of row
                result = 0;
            }
        } else if (damagedList.isEmpty()) {
            if (row.contains("#")) {
                // Fail: Leftover hashes
                result = 0;
            } else {
                // Arrangement found; assume the remaining machines all work.
                result = 1;
            }
        } else {
            var mWorking = R_WORKING.matcher(row);
            if (mWorking.matches()) {
                result = findArrangements(row.substring(mWorking.group(1).length()), damagedList);
            } else {
                result = 0;
                if (row.charAt(0) == '?') {
                    // Assume this machine works.
                    result += findArrangements(row.substring(1), damagedList);
                }

                short currentDamaged = damagedList.get(0);
                var mPossiblyBroken = R_POSSIBLY_BROKEN_FULL.get(currentDamaged).matcher(row);
                if (mPossiblyBroken.matches()) {
                    List<Short> damagedRest = damagedList.subList(1, damagedList.size());
                    // Assume all machines in this range are broken.
                    result += findArrangements(
                            row.substring(mPossiblyBroken.group(1).length()), damagedRest);
                }
            }
        }
        cache.put(cacheKey, result);
        return result;
    }

    public static void main(String[] args) throws IOException {
        List<String> lines = Files.readAllLines(Paths.get("12.txt"), StandardCharsets.UTF_8);
        int result = 0;
        for (var line : lines) {
            String[] split1 = line.split(" ");
            String row = split1[0];
            String[] damageStrs = split1[1].split(",");
            List<Short> damagedList = Arrays.stream(damageStrs).map(Short::parseShort)
                    .collect(Collectors.toList());

            long arrangements = new Adv12().findArrangements(row, damagedList);
            result += arrangements;
        }
        System.out.println("Part 1: " + result);

        long result2 = 0;
        for (var line : lines) {
            String[] split1 = line.split(" ");
            List<String> fiveRows = Arrays.asList(split1[0], split1[0], split1[0], split1[0], split1[0]);
            String row = String.join("?", fiveRows);
            List<String> fiveDamageStrs = Arrays.asList(split1[1], split1[1], split1[1], split1[1], split1[1]);
            String damageStrs = String.join(",", fiveDamageStrs);
            String[] damageStrsSplit = damageStrs.split(",");
            List<Short> damagedList = Arrays.stream(damageStrsSplit).map(Short::parseShort)
                    .collect(Collectors.toList());

            long arrangements = new Adv12().findArrangements(row, damagedList);
            // System.out.println(line + " -> " + arrangements);
            result2 += arrangements;
        }

        System.out.println("Part 2: " + result2);
    }
}
