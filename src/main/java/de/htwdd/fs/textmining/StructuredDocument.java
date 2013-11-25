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

import gate.*;

import java.util.*;

public class StructuredDocument {

    private final Set<String> ANNOTATIONS_REQUIRED = new HashSet<String>();

    private String plain;
    private String annotatedXML;

    public StructuredDocument(String plain) throws Exception {
        this.plain  = plain;

        // TODO test if we need more to find all patterns or change something
        ANNOTATIONS_REQUIRED.add("NNP");
        ANNOTATIONS_REQUIRED.add("NN");
        ANNOTATIONS_REQUIRED.add("NNS");

        analysePlain();
    }

    public String getPlain() {
        return plain;
    }

    public void setPlain(String plain) throws Exception {
        this.plain = plain;

        analysePlain();
    }

    public String getAnnotatedXML() {
        return this.annotatedXML;
    }

    private void analysePlain() throws Exception {
        ANNIE                annie;
        Corpus               corpus;
        FeatureMap           params;
        Document             document;
        Iterator<Annotation> itr;
        SortedAnnotationList sortedAnnotationList;
        Annotation           currentAnnotation;
        StringBuffer         editableContent;
        long                 insertPositionStart;
        long                 insertPositionEnd;

        annie  = new ANNIE();
        corpus = (Corpus) Factory.createResource("gate.corpora.CorpusImpl");

        params = Factory.newFeatureMap();
        params.put("stringContent", this.plain);
        params.put("preserveOriginalContent", true);
        params.put("collectRepositioningInfo", true);

        document = (Document) Factory.createResource("gate.corpora.DocumentImpl", params);

        corpus.add(document);
        annie.setCorpus(corpus);
        annie.execute();

        itr                  = document.getAnnotations().iterator();
        sortedAnnotationList = new SortedAnnotationList();

        while (itr.hasNext()) {
            Annotation current = itr.next();

            if (ANNOTATIONS_REQUIRED.contains(current.getFeatures().get("category"))) {
                sortedAnnotationList.addSortedExclusive(current);
            } // no else
        }

        editableContent = new StringBuffer(this.plain);

        for (int i = sortedAnnotationList.size() - 1; i >= 0; --i) {
            currentAnnotation   = sortedAnnotationList.get(i);
            insertPositionStart = currentAnnotation.getStartNode().getOffset();
            insertPositionEnd   = currentAnnotation.getEndNode().getOffset();

            if (-1 != insertPositionStart && -1 != insertPositionEnd) {
                // identify found elements with:   \{\{.*\}\}
                editableContent.insert((int) insertPositionEnd,   "}}");
                editableContent.insert((int) insertPositionStart, "{{");
            }
        }

        annotatedXML = editableContent.toString();
    }

    private class SortedAnnotationList extends Vector<Annotation> {
        public SortedAnnotationList() {
            super();
        }

        public boolean addSortedExclusive(Annotation annotation) {
            Annotation currentAnnotation;
            long       annotationStart;
            long       currentStart;

            for (int i = 0; i < this.size(); i++) {
                currentAnnotation = this.get(i);

                if (annotation.overlaps(currentAnnotation)) {
                    return false;
                } // no else
            }

            annotationStart = annotation.getStartNode().getOffset();

            for (int i = 0; i < this.size(); i++) {
                currentAnnotation = this.get(i);
                currentStart      = currentAnnotation.getStartNode().getOffset();

                if (annotationStart < currentStart) {
                    this.insertElementAt(annotation, i);

                    return true;
                } // no else
            }

            this.insertElementAt(annotation, this.size());
            return true;
        }
    }

}
