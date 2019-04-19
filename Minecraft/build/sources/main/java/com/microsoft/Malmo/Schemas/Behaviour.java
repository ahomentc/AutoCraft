//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.4 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2019.04.10 at 11:48:38 AM PDT 
//


package com.microsoft.Malmo.Schemas;

import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlEnumValue;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for Behaviour.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * <p>
 * <pre>
 * &lt;simpleType name="Behaviour">
 *   &lt;restriction base="{http://www.w3.org/2001/XMLSchema}string">
 *     &lt;enumeration value="onceOnly"/>
 *     &lt;enumeration value="oncePerBlock"/>
 *     &lt;enumeration value="oncePerTimeSpan"/>
 *     &lt;enumeration value="constant"/>
 *   &lt;/restriction>
 * &lt;/simpleType>
 * </pre>
 * 
 */
@XmlType(name = "Behaviour")
@XmlEnum
public enum Behaviour {

    @XmlEnumValue("onceOnly")
    ONCE_ONLY("onceOnly"),
    @XmlEnumValue("oncePerBlock")
    ONCE_PER_BLOCK("oncePerBlock"),
    @XmlEnumValue("oncePerTimeSpan")
    ONCE_PER_TIME_SPAN("oncePerTimeSpan"),
    @XmlEnumValue("constant")
    CONSTANT("constant");
    private final String value;

    Behaviour(String v) {
        value = v;
    }

    public String value() {
        return value;
    }

    public static Behaviour fromValue(String v) {
        for (Behaviour c: Behaviour.values()) {
            if (c.value.equals(v)) {
                return c;
            }
        }
        throw new IllegalArgumentException(v);
    }

}
