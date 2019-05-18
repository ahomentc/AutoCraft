//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.4 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2019.05.18 at 03:45:40 PM PDT 
//


package com.microsoft.Malmo.Schemas;

import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for Facing.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * <p>
 * <pre>
 * &lt;simpleType name="Facing">
 *   &lt;restriction base="{http://www.w3.org/2001/XMLSchema}string">
 *     &lt;enumeration value="DOWN"/>
 *     &lt;enumeration value="UP"/>
 *     &lt;enumeration value="NORTH"/>
 *     &lt;enumeration value="SOUTH"/>
 *     &lt;enumeration value="WEST"/>
 *     &lt;enumeration value="EAST"/>
 *     &lt;enumeration value="UP_X"/>
 *     &lt;enumeration value="DOWN_X"/>
 *     &lt;enumeration value="UP_Z"/>
 *     &lt;enumeration value="DOWN_Z"/>
 *   &lt;/restriction>
 * &lt;/simpleType>
 * </pre>
 * 
 */
@XmlType(name = "Facing")
@XmlEnum
public enum Facing {

    DOWN,
    UP,
    NORTH,
    SOUTH,
    WEST,
    EAST,
    UP_X,
    DOWN_X,
    UP_Z,
    DOWN_Z;

    public String value() {
        return name();
    }

    public static Facing fromValue(String v) {
        return valueOf(v);
    }

}
