/**
 * Copyright 2013 Torsten Braun
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package de.htwdd.fs.textmining.pattern_matching;

import de.htwdd.fs.textmining.StructuredDocument;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public abstract class TMPattern {

    protected StructuredDocument           document;
    protected Map<String, Set<String>> elements;

    public TMPattern(StructuredDocument document) {
        this.document = document;
        elements      = new HashMap<String, Set<String>>();

        patternMatcher();
    }

    abstract protected void patternMatcher();

    public Map<String, Set<String>> getElements() {
        return this.elements;
    }

    public Set<String> get(String key) {
        return this.elements.get(key);
    }

}
