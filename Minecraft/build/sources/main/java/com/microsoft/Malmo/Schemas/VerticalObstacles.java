//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.4 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2019.04.10 at 11:48:38 AM PDT 
//


package com.microsoft.Malmo.Schemas;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for VerticalObstacles complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="VerticalObstacles">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;all>
 *         &lt;element name="stairs" type="{http://ProjectMalmo.microsoft.com}NonNegative"/>
 *         &lt;element name="ladder" type="{http://ProjectMalmo.microsoft.com}NonNegative"/>
 *         &lt;element name="jump" type="{http://ProjectMalmo.microsoft.com}NonNegative"/>
 *       &lt;/all>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "VerticalObstacles", propOrder = {

})
public class VerticalObstacles {

    protected int stairs;
    protected int ladder;
    protected int jump;

    /**
     * Gets the value of the stairs property.
     * 
     */
    public int getStairs() {
        return stairs;
    }

    /**
     * Sets the value of the stairs property.
     * 
     */
    public void setStairs(int value) {
        this.stairs = value;
    }

    /**
     * Gets the value of the ladder property.
     * 
     */
    public int getLadder() {
        return ladder;
    }

    /**
     * Sets the value of the ladder property.
     * 
     */
    public void setLadder(int value) {
        this.ladder = value;
    }

    /**
     * Gets the value of the jump property.
     * 
     */
    public int getJump() {
        return jump;
    }

    /**
     * Sets the value of the jump property.
     * 
     */
    public void setJump(int value) {
        this.jump = value;
    }

}
