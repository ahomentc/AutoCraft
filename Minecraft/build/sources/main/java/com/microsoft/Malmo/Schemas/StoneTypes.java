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
 * <p>Java class for StoneTypes.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * <p>
 * <pre>
 * &lt;simpleType name="StoneTypes">
 *   &lt;restriction base="{http://www.w3.org/2001/XMLSchema}string">
 *     &lt;enumeration value="stone"/>
 *     &lt;enumeration value="granite"/>
 *     &lt;enumeration value="smooth_granite"/>
 *     &lt;enumeration value="diorite"/>
 *     &lt;enumeration value="smooth_diorite"/>
 *     &lt;enumeration value="andesite"/>
 *     &lt;enumeration value="smooth_andesite"/>
 *   &lt;/restriction>
 * &lt;/simpleType>
 * </pre>
 * 
 */
@XmlType(name = "StoneTypes")
@XmlEnum
public enum StoneTypes {

    @XmlEnumValue("stone")
    STONE("stone"),
    @XmlEnumValue("granite")
    GRANITE("granite"),
    @XmlEnumValue("smooth_granite")
    SMOOTH_GRANITE("smooth_granite"),
    @XmlEnumValue("diorite")
    DIORITE("diorite"),
    @XmlEnumValue("smooth_diorite")
    SMOOTH_DIORITE("smooth_diorite"),
    @XmlEnumValue("andesite")
    ANDESITE("andesite"),
    @XmlEnumValue("smooth_andesite")
    SMOOTH_ANDESITE("smooth_andesite");
    private final String value;

    StoneTypes(String v) {
        value = v;
    }

    public String value() {
        return value;
    }

    public static StoneTypes fromValue(String v) {
        for (StoneTypes c: StoneTypes.values()) {
            if (c.value.equals(v)) {
                return c;
            }
        }
        throw new IllegalArgumentException(v);
    }

}
