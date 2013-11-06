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

package de.htwdd.fs.textmining;

import gate.Annotation;

import java.util.HashMap;
import java.util.Map;

public class StructuredDocument {

    private String plain;

    private Map<Position, Annotation> annotations;

    public StructuredDocument(String plain) {
        this.plain  = plain;
        annotations = new HashMap<Position, Annotation>();

        analysePlain();
    }

    public String getPlain() {
        return plain;
    }

    public void setPlain(String plain) {
        this.plain = plain;

        analysePlain();
    }

    public Map<Position, Annotation> getAnnotations() {
        return annotations;
    }

    private void addAnnotation(Position position, Annotation annotation) {
        annotations.put(position, annotation);
    }

    private void analysePlain() {
        // TODO
    }

    private class Position {

        private int x1;
        private int x2;

        private Position(int x1, int x2) {
            this.x1 = x1;
            this.x2 = x2;
        }

        public int getX1() {
            return x1;
        }

        public void setX1(int x1) {
            this.x1 = x1;
        }

        public int getX2() {
            return x2;
        }

        public void setX2(int x2) {
            this.x2 = x2;
        }
    }

}
