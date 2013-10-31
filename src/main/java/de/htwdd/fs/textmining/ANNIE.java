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
import gate.Gate;
import gate.creole.ANNIEConstants;
import gate.creole.ExecutionException;
import gate.creole.SerialAnalyserController;
import gate.util.persistence.PersistenceManager;
import org.apache.log4j.Logger;

import java.io.File;

public class ANNIE {

    private final Logger LOGGER = Logger.getLogger(ANNIE.class);

    private SerialAnalyserController annieController;

    public ANNIE() throws Exception {
        initANNIE();
    }

    /**
     * Set the corpus for ANNIE.
     *
     * @param corpus
     */
    public void setCorpus(Corpus corpus) {
        annieController.setCorpus(corpus);
    }

    public void execute() throws ExecutionException {
        annieController.execute();
    }

    /**
     * Initialize ANNIE and create a corpus pipline.
     */
    private void initANNIE() throws Exception {
        annieController = (SerialAnalyserController) PersistenceManager.loadObjectFromFile(
                new  File(
                        new File(Gate.getPluginsHome(), ANNIEConstants.PLUGIN_DIR),
                        ANNIEConstants.DEFAULT_FILE
                )
        );
    }
}