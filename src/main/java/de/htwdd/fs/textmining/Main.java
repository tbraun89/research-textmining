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

import gate.Gate;
import org.apache.log4j.Logger;

import java.io.File;

public class Main {

    private final static Logger LOGGER = Logger.getLogger(Main.class);

    public static void main(String[] args) {
        ANNIE   annie;

        try {
            initGate();
            annie = new ANNIE();
        } catch (Exception e) {
            LOGGER.error(e.getMessage());
            System.exit(1);
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
            LOGGER.warn(e.getMessage());
        }
        Gate.init();

        gateHome    = Gate.getGateHome();
        pluginsHome = new File(gateHome, "plugins");

        Gate.getCreoleRegister().registerDirectories(new File(pluginsHome, "ANNIE").toURI().toURL());
    }

}
