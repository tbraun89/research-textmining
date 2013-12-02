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

import de.htwdd.fs.textmining.pattern_matching.HearstPattern;
import gate.Gate;
import org.apache.commons.io.FileUtils;
import org.apache.log4j.Logger;

import java.io.File;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Scanner;

public class RunFullCorpus {

    private static Logger logger = Logger.getLogger(RunFullCorpus.class);

    public static void main(String[] args) throws Exception {
        RunFullCorpus app = new RunFullCorpus();

        if (1 != args.length) {
            System.out.println("Usage: RunFullCorpus CORPUS_ROOT_DIR");
            System.exit(1);
        } // no else

        initGate();

        for (File currentFile : app.getFileList(new File(args[0]))) {
            app.processFile(currentFile);
        }
    }

    private ArrayList<File> getFileList(File path) {
        ArrayList<File> fileList = new ArrayList<File>();
        Iterator        itr      = FileUtils.iterateFiles(path, new String[] {"txt"}, true);

        logger.info("Scanning files in: \"" + path + "\"...");

        while (itr.hasNext()) {
            fileList.add((File) itr.next());
        }

        logger.info(fileList.size() + " files found.");

        return fileList;
    }

    private void processFile(File file) {
        String             content;
        StructuredDocument document;
        HearstPattern      patternMatcher;

        logger.info("Processing: \"" + file.getAbsoluteFile() + "\"");

        try {
            content  = new Scanner(file).useDelimiter("\\Z").next();
            document = new StructuredDocument(content);

            patternMatcher = new HearstPattern(document);
            patternMatcher.getElements(); // TODO store elements in global dictionary/database
        } catch (Exception e) {
            logger.error("Parsing failed: " + e.getMessage());
        }
    }

    /**
     * Initialize Gate and load all plugins.
     */
    protected static void initGate() throws Exception {
        File gateHome;
        File pluginsHome;

        try {
            Gate.setGateHome(new File(Main.class.getResource("/gate").toURI()));
        } catch (IllegalStateException e) {
            logger.warn(e.getMessage());
        }
        Gate.init();

        gateHome    = Gate.getGateHome();
        pluginsHome = new File(gateHome, "plugins");

        Gate.getCreoleRegister().registerDirectories(new File(pluginsHome, "ANNIE").toURI().toURL());
    }
}
