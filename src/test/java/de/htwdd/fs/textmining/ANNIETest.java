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

import gate.Corpus;
import gate.Factory;
import gate.creole.ExecutionException;
import org.junit.BeforeClass;
import org.junit.Test;

public class ANNIETest {

    private static ANNIE annie;

    @BeforeClass
    public static void setup() {
        Main.initGate();
        annie = new ANNIE();
    }

    @Test
    public void setCorpus() throws Exception {
        Corpus corpus = (Corpus) Factory.createResource("gate.corpora.CorpusImpl");

        annie.setCorpus(null);
        annie.setCorpus(corpus);
    }

    @Test(expected = ExecutionException.class)
    public void executeWithoutCorpus() throws Exception {
        annie.execute();
    }

    @Test
    public void execute() throws Exception {
        Corpus corpus = (Corpus) Factory.createResource("gate.corpora.CorpusImpl");

        annie.setCorpus(corpus);
        annie.execute();
    }

}
