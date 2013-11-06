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

import org.junit.Test;
import static org.junit.Assert.*;

public class StructuredDocumentTest {

    private final String DEMO_PAIN_TEXT = "This is a demo from Dresden about Hans Peter Jackson.";

    @Test
    public void plain() throws Exception {
        StructuredDocument document;
        String             newPlainText;

        document = new StructuredDocument(DEMO_PAIN_TEXT);

        assertEquals(DEMO_PAIN_TEXT, document.getPlain());

        newPlainText = new String("Changed plain Text.");
        document.setPlain(newPlainText);

        assertEquals(newPlainText, document.getPlain());
    }

}
