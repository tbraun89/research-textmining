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

import gate.Factory;
import gate.FeatureMap;
import gate.wordnet.Synset;
import gate.wordnet.WordNet;
import gate.wordnet.WordSense;

import java.util.List;

public class WordNetMatcher {

    private WordNet wordNet;

    public WordNetMatcher() throws Exception {
        FeatureMap featureMap;

        featureMap   = Factory.newFeatureMap();
        featureMap.put("propertyUrl", WordNetMatcher.class.getResource("/wordnet.xml"));

        this.wordNet = (WordNet) Factory.createResource("gate.wordnet.JWNLWordNetImpl", featureMap);
    }

    public boolean isMatching(String hyponym, String hypernym) throws Exception {
        List<WordSense> senseList;
        WordSense       currentSense;
        Synset          currentSynset;
        boolean         result = false;

        senseList = this.wordNet.lookupWord(hyponym, WordNet.POS_NOUN);
        assert senseList.size() == 8;

        for (int i = 0; i < senseList.size(); i++) {
            currentSense  = senseList.get(i);
            currentSynset = currentSense.getSynset();
            assert currentSynset != null;

            result = false; // TODO check hypernym with the looked up word
        }

        return result;
    }

}
