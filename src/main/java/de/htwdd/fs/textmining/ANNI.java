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

import java.io.File;

public class ANNI {

    public static void main(String args[]) throws Exception {
        File gateHome;
        File pluginsHome;

        System.out.println("Initializing Gate...");
        Gate.setGateHome(new File("resources/gate"));
        Gate.init();

        gateHome    = Gate.getGateHome();
        pluginsHome = new File(gateHome, "plugins");

        System.out.println("Loading ANNIE...");
        Gate.getCreoleRegister().registerDirectories(new File(pluginsHome, "ANNIE").toURI().toURL());
    }

}