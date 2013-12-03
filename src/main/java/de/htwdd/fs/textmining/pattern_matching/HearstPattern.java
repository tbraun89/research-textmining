package de.htwdd.fs.textmining.pattern_matching;

import de.htwdd.fs.textmining.StructuredDocument;

import java.util.HashSet;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class HearstPattern extends TMPattern {

    public HearstPattern(StructuredDocument document) {
        super(document);
    }

    @Override
    protected void patternMatcher() {
        Pattern     pattern    = Pattern.compile("<np>(\\w+)</np> such as|\\G(?<!^)(?:,| or| and)? <np>(\\w+)</np>");
        Matcher     matcher    = pattern.matcher(document.getAnnotatedString());
        String      currentKey = "";
        Set<String> currentSet;

        while (matcher.find()) {
            if (null != matcher.group(1)) {
                currentKey = matcher.group(1);
            } else {
                if (elements.containsKey(currentKey)) {
                    currentSet = elements.get(currentKey);
                    currentSet.add(matcher.group(2));
                    elements.put(currentKey, currentSet);
                } else {
                    currentSet = new HashSet<String>();
                    currentSet.add(matcher.group(2));
                    elements.put(currentKey, currentSet);
                }
            }
        }
    }

}
